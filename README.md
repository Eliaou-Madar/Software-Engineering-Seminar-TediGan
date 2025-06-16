Notre framework TediGan peut produire divers résultats pour la génération et la manipulation d'images faciales avec un guidage textuel.

Étant donné une description textuelle, la génération de texte en image peut produire des images cohérentes avec le texte. Étant donné un texte et une image, la manipulation d'image guidée par texte consiste à modifier les attributs pertinents uniquement en gardant inchangés ceux qui ne sont pas liés.

Notre méthode unifie pour la première fois deux tâches différentes dans le même cadre et atteint une grande accessibilité, diversité, contrôlabilité et précision pour la génération et la manipulation d'images faciales. Grâce à la conception du réseau, notre méthode prend en charge de manière inhérente les opérations continues, génération haute résolution et synthèse multimodale pour les croquis et les étiquettes sémantiques avec descriptions.

![image](https://github.com/user-attachments/assets/9c91759d-8701-4c13-a463-ecb15688cd7a)


Ensemble de données texte-image

Pour réaliser la génération et la manipulation d'images guidées par texte, la première étape consiste à créer un ensemble de données contenant des images faciales photoréalistes et les descriptions correspondantes. Il existe actuellement deux ensembles de données de synthèse texte-image populaires : cub pour les oiseaux et cacao pour les scènes naturelles. Pour combler les lacunes dans l'ensemble de données de synthèse texte-image pour les visages, en suivant le format des deux ensembles de données populaires susmentionnés, nous créons 10 descriptions uniques pour chaque image dans la célébrité ahq. L'ensemble de données ahq multimodal de célébrités introduit est un ensemble de données d'images de visage à grande échelle qui contient 30 000 images de visage haute résolution, chacune ayant un masque de segmentation de haute qualité, un texte descriptif et une image avec un arrière-plan transparent.
Vous pouvez retrouver sur ce GitHub le code qui a permis de générer le jeu de données (texte, sketch, labels, suppression de l’arrière-plan).

![image](https://github.com/user-attachments/assets/2c34e8d4-d7ee-462f-af4f-2a7da948e09d)


Idée clé du cadre et inversion

L'idée clé de notre cadre est de mapper notre image texte TediGAN et d'autres modalités dans l'espace latent d'un générateur de style gone pré-entraîné où les informations multimodales peuvent apprendre les relations de correspondance et faire les alignements correspondants entre le texte et l'image. Pour ce faire, nous apprenons d'abord l'inversion qui consiste à entraîner un encodeur d'image à mapper les images réelles à l'espace latent de telle sorte que tous les codes produits par l'encodeur puissent être récupérés à la fois au niveau du pixel et au niveau sémantique.

Nous utilisons ensuite la caractéristique hiérarchique de l'espace w pour apprendre la correspondance texte-image en mappant le texte dans le même espace latent conjoint partagé avec l'intégration visuelle. La représentation par couche du style gone apprend le démêlage des fragments sémantiques, des attributs ou des objets. L'intégration visuelle et l'intégration linguistique ont la même forme l fois c, ce qui signifie avoir l couches dans chacune avec un code latent à c dimensions. Le mécanisme de contrôle peut sélectionner des attributs de couches spécifiques et mélanger ces couches du code de style en remplaçant partiellement les couches de contenu correspondantes pour préserver l'identité et la manipulation.

Module d’inversion StyleGAN

Le module d'inversion vise à former un encodeur d'image d'inversion StyleGAN qui peut mapper un réelImage du visage dans l'espace latent d'un modèle gone de style fixe pré-entraîné sur le jeu de données ffhq. La raison pour laquelle nous inversons un modèle gone entraîné au lieu d'en former un à partir de zéro est que de cette façon, nous pouvons aller au-delà des limites d'un jeu de données d'images de texte appariées. Le style gone est entraîné dans un environnement non supervisé et couvre une qualité bien supérieure et une plus grande diversité, ce qui rend notre méthode capable de produire des résultats édités satisfaisants avec des images dans la nature afin de faciliter l'alignement ultérieur avec les attributs de texte.
Notre objectif pour l'inversion n'est pas seulement de reconstruire l'image d'entrée par valeurs de pixels, mais aussi d'acquérir le code inversé qui est sémantiquement significatif et interprétable. Le processus d'apprentissage de l'encodeur d'image peut être formulé comme les fonctions objectives grâce à l'encodeur d'image appris. Nous pouvons mapper une image réelle dans l'espace w et obtenir un code latent w. w est le code projeté de l'incorporation z dans l'espace latent d'entrée z en utilisant un réseau de mappage non linéaire f implémenté à l'aide d'un MLP à huit couches. Le code obtenu est garanti pour s'aligner sur le domaine sémantique du générateur de style gone et peut être utilisé pour exploiter le cross-modal.

![image](https://github.com/user-attachments/assets/8bc93471-31f6-4530-96d1-3eb68894ddcd)


Similarité visuo-linguistique

Une fois le module d'inversion entraîné, étant donné une image réelle, nous pouvons la mapper dans l'espace w du style gone. Le problème suivant est de savoir comment entraîner un encodeur de texte qui apprend les associations et les alignements entre l'image et le texte au lieu d'entraîner un encodeur de texte de la même manière que l'encodeur d'image. Nous proposons un module de similarité visuo-linguistique pour projeter l'image et le texte dans un espace d'intégration commun, l'espace w. Étant donné une image réelle et ses descriptions, nous les encodons dans l'espace w en utilisant l'encodeur d'image précédemment entraîné et un encodeur de texte. Le code latent obtenu est la concaténation de l vecteurs w de dimension c différents, un pour chaque couche d'entrée du style gone. L'alignement multimodal peut être entraîné avec la fonction objective. Ce module réalise l'alignement au niveau de l'instance, c'est-à-dire l'apprentissage des correspondances entre les attributs visuels et linguistiques en exploitant la démêlabilité du style gone.

![image](https://github.com/user-attachments/assets/3fbc1fb0-4ac1-4c6f-9e73-6625e7193612)


Optimisation au niveau de l’instance

L'un des principaux défis de l'optimisation au niveau de l'instance du visage est la préservation de l'identité en raison de la capacité de représentation limitée. Apprendre un mappage inverse parfait avec un encodeur seul n'est pas facile pour préserver l'identité. Certaines méthodes récentes intègrent une perte de reconnaissance faciale dédiée pour mesurer la similarité cosinus entre l'image de sortie et sa source. Différente de leurs méthodes de manipulation d'image guidée par texte, nous implémentons un module d'optimisation au niveau de l'instance pour manipuler précisément les attributs souhaités cohérents avec les descriptions tout en reconstruisant fidèlement ceux qui ne sont pas concernés. Nous utilisons le code de voie inversé z comme initialisation et l'encodeur d'image est inclus comme régularisation pour préserver le code de voie dans le domaine sémantique du générateur. La fonction objective pourL'optimisation est résumée comme suit : les deux tâches différentes, à savoir la génération d'images de texte et la manipulation d'images guidées par le texte, sont unifiées en un seul cadre par notre mécanisme de contrôle proposé.

![image](https://github.com/user-attachments/assets/fb502d55-ae45-47ef-9148-a190a673767b)


Mécanisme de contrôle par mélange de styles

Notre mécanisme est basé sur le mélange de styles. La représentation par couches du style appris démêle les fragments sémantiques, les attributs ou les objets en général. La couche de glace du code latent représente différents attributs et est introduite dans la couche de glace du générateur. La modification de la valeur d'une certaine couche modifierait les attributs correspondants de l'image.

Étant donné deux codes de même taille, le code de style wc avec la forme l fois c indiquant le code de contenu et le code de style. Ce mécanisme de contrôle sélectionne des attributs de couches spécifiques et mélange ces couches du code de style en remplaçant partiellement les couches correspondantes du contenu pour la génération de texte en image. Les images produites doivent être cohérentes avec la description textuelle.
Le code de contenu doit donc être le code linguistique et le code de voie échantillonné de manière aléatoire avec la même taille agit comme code de style pour fournir de la diversité pour la manipulation d'images guidée par le texte. Le code de contenu est l'intégration visuelle tandis que le code de style est l'intégration linguistique. Les couches à mélanger doivent être pertinentes pour le texte afin de modifier les attributs pertinents.

Français : seulement en gardant les éléments non liés inchangés pour produire les divers résultats. Tout ce que nous devons faire est de garder les couches liées au texte inchangées et de remplacer les autres par le code latent ws échantillonné aléatoirement et le code de contenu wc pourrait être une image d'étiquette de croquis et du bruit qui rend notre pistolet en peluche réalisable pour la synthèse d'images à partir d'entrées multimodales.

En raison du mécanisme de contrôle, notre méthode prend en charge de manière inhérente la synthèse d'images à partir d'entrées multimodales telles que des croquis et des étiquettes sémantiques avec des descriptions. Par exemple, si nous voulons générer des images à partir d'une autre modalité avec un guidage textuel, prenons le croquis comme exemple : nous pouvons entraîner un encodeur d'image de croquis supplémentaire de la même manière que l'encodeur d'image réelle et laisser les autres parties inchangées.

Haute résolution et variations stochastiques

Notre méthode est également capable de générer des images 10 24 x 10 24 de haute qualité. Les images haute résolution contiennent beaucoup de détails faciaux et ne peuvent pas être obtenues par un simple échantillonnage à partir des résolutions inférieures, rendant les variations stochastiques particulièrement importantes car elles améliorent la perception visuelle sans affecter les principales structures et attributs de l'image synthétisée.

Les méthodes précédentes produisent des résultats qui ressemblent à une simple combinaison d'attributs visuels de différentes échelles d'image. Certains des attributs contenus dans le texte n'apparaissent pas dans l'image générée et l'image générée ressemble à une peinture sans relief et manque de détails. Cet aspect pictural sans relief serait considérablement évident et irrémédiable lors de la génération d'images à plus haute résolution en utilisant les méthodes actuelles. Notre méthode peut produire des images diverses et de haute qualité avec une résolution sans précédent à 10 24.

Analyse par calque et évaluation

En général, les calques du générateur à basse résolution contrôlent les styles de haut niveau tels que les lunettes et la pose de la tête. Les calques du milieu contrôlent la coiffure et l'expression faciale, tandis que les calques finaux contrôlent les schémas de couleurs et les détails fins. Nous effectuons une analyse par calque sur le style pré-entraîné que nous avons utilisé dans la plupart des expériences, qui consiste à générer des images de 256 fois 256 et qui comporte 14 calques du vecteur intermédiaire, en nous basant sur les observations empiriques. Nous listons les attributs représentés par les différentes calques d'un style de 14 calques dans le tableau. Les calques de 11 à 14 représentent des micro-caractéristiques ou des structures fines telles que des taches de rousseur ou des pores de la peau, qui peuvent être considérés comme la variation stochastique. Ces variations stochastiques sont particulièrement importantes pour les images haute résolution car elles produisent beaucoup de détails du visage et améliorent la perception visuelle sans affecter les principales structures et attributs de l'image synthétisée.

Nous évaluons notre méthode proposée sur la comparaison de texte et les partitions d'images en la comparant aux approches de pointe et en contrôlant gone dmgon et dfgon pour la génération d'images et en la comparant à montegon pour la manipulation d'images en langage naturel. descriptions: toutes les méthodes sont recyclées avec les paramètres par défaut sur l'ensemble de données multimodal celeb ahq proposé.
Nous illustrons également la comparaison de l'esquisse à l'image et de l'étiquette à la génération d'image. Ces résultats expérimentaux démontrent la supériorité de notre méthode en termes d'efficacité de la synthèse d'images, la capacité de générer des résultats de haute qualité et l'extensibilité pour les entrées multimodales.

Mercidémontrer la supériorité de notre méthode en termes d'efficacité de synthèse d'images, de capacité à générer des résultats de haute qualité et d'extensibilité pour les entrées multimodales. Mercidémontrer la supériorité de notre méthode en termes d'efficacité de synthèse d'images, de capacité à générer des résultats de haute qualité et d'extensibilité pour les entrées multimodales.
