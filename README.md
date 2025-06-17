Notre framework TediGan peut produire divers résultats pour la génération et la manipulation d'images faciales avec un guidage textuel.

Étant donné une description textuelle, la génération de texte en image peut produire des images cohérentes avec le texte. Étant donné un texte et une image, la manipulation d'image guidée par texte consiste à modifier les attributs pertinents uniquement en gardant inchangés ceux qui ne sont pas liés.

Notre méthode unifie pour la première fois deux tâches différentes dans le même cadre et atteint une grande accessibilité, diversité, contrôlabilité et précision pour la génération et la manipulation d'images faciales. Grâce à la conception du réseau, notre méthode prend en charge de manière inhérente les opérations continues, génération haute résolution et synthèse multimodale pour les croquis et les étiquettes sémantiques avec descriptions.

![image](https://github.com/user-attachments/assets/9c91759d-8701-4c13-a463-ecb15688cd7a)


Ensemble de données texte-image

Pour réaliser la génération et la manipulation d'images guidées par texte, la première étape consiste à créer un ensemble de données contenant des images faciales photoréalistes et les descriptions correspondantes. Il existe actuellement deux ensembles de données de synthèse texte-image populaires : cub pour les oiseaux et cacao pour les scènes naturelles. Pour combler les lacunes dans l'ensemble de données de synthèse texte-image pour les visages, en suivant le format des deux ensembles de données populaires susmentionnés, nous créons 10 descriptions uniques pour chaque image dans la célébrité ahq. L'ensemble de données ahq multimodal de célébrités introduit est un ensemble de données d'images de visage à grande échelle qui contient 30 000 images de visage haute résolution, chacune ayant un masque de segmentation de haute qualité, un texte descriptif et une image avec un arrière-plan transparent.
Vous pouvez retrouver sur ce GitHub le code qui a permis de générer le jeu de données (texte, sketch, labels, suppression de l’arrière-plan).

![image](https://github.com/user-attachments/assets/2c34e8d4-d7ee-462f-af4f-2a7da948e09d)


Idée clé du cadre et inversion

L'idée clé de notre cadre est de mapper notre image texte TediGAN et d'autres modalités dans l'espace latent d'un générateur de StyleGan pré-entraîné où les informations multimodales peuvent apprendre les relations de correspondance et faire les alignements correspondants entre le texte et l'image. Pour ce faire, nous apprenons d'abord l'inversion qui consiste à entraîner un encodeur d'image à mapper les images réelles à l'espace latent de telle sorte que tous les codes produits par l'encodeur puissent être récupérés à la fois au niveau du pixel et au niveau sémantique.

Nous utilisons ensuite la caractéristique hiérarchique de l'espace w pour apprendre la correspondance texte-image en mappant le texte dans le même espace latent conjoint partagé avec l'intégration visuelle. La représentation par couche du style gone apprend le démêlage des fragments sémantiques, des attributs ou des objets. L'intégration visuelle et l'intégration linguistique ont la même forme l fois c, ce qui signifie avoir l couches dans chacune avec un code latent à c dimensions. Le mécanisme de contrôle peut sélectionner des attributs de couches spécifiques et mélanger ces couches du code de style en remplaçant partiellement les couches de contenu correspondantes pour préserver l'identité et la manipulation.

![image](https://github.com/user-attachments/assets/82d7c236-745e-426a-bede-87d144f76802)


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

Étant donné deux codes de même taille, le code de style wc avec la forme l fois c indiquant le code de contenu et le code de style. Ce mécanisme de contrôle sélectionne des attributs de couches spécifiques et mélange ces couches du code de style en remplaçant partiellement les couches correspondantes du contenu.

![image](https://github.com/user-attachments/assets/7c5bd0d6-f69e-4c48-a396-06dc2a83188d)

Pour la génération de texte en image.

Les images produites doivent être cohérentes avec la description textuelle.
Le code de contenu doit donc être le code linguistique et le code de voie échantillonné de manière aléatoire avec la même taille agit comme code de style pour fournir de la diversité.

![image](https://github.com/user-attachments/assets/ac60e237-3c1c-4865-abeb-dfaaf45101be)


Pour la manipulation d'images guidée par le texte.

Le code de contenu est l'intégration visuelle tandis que le code de style est l'intégration linguistique. Les couches à mélanger doivent être pertinentes pour le texte afin de modifier les attributs pertinents.

![image](https://github.com/user-attachments/assets/a8de79b3-8fdb-4bd9-8d11-38812aa28c72)



Seulement en gardant les éléments non liés inchangés pour produire les divers résultats. Tout ce que nous devons faire est de garder les couches liées au texte inchangées et de remplacer les autres par le code latent ws échantillonné aléatoirement et le code de contenu wc pourrait être une image d'étiquette de croquis et du bruit qui rend notre pistolet en peluche réalisable pour la synthèse d'images à partir d'entrées multimodales.

![image](https://github.com/user-attachments/assets/76a7b059-6087-47bf-8227-b5d3620977e1)


En raison du mécanisme de contrôle, notre méthode prend en charge de manière inhérente la synthèse d'images à partir d'entrées multimodales telles que des croquis et des étiquettes sémantiques avec des descriptions. Par exemple, si nous voulons générer des images à partir d'une autre modalité avec un guidage textuel, prenons le croquis comme exemple : nous pouvons entraîner un encodeur d'image de croquis supplémentaire de la même manière que l'encodeur d'image réelle et laisser les autres parties inchangées.

![image](https://github.com/user-attachments/assets/139a6599-9053-4131-8275-2365f35a343a)


Haute résolution et variations stochastiques

Notre méthode est également capable de générer des images 1024 x 1024 de haute qualité. Les images haute résolution contiennent beaucoup de détails faciaux et ne peuvent pas être obtenues par un simple échantillonnage à partir des résolutions inférieures, rendant les variations stochastiques particulièrement importantes car elles améliorent la perception visuelle sans affecter les principales structures et attributs de l'image synthétisée.

![image](https://github.com/user-attachments/assets/bf277ed5-6161-455d-828c-9fb897c91ecb)


Les méthodes précédentes produisent des résultats qui ressemblent à une simple combinaison d'attributs visuels de différentes échelles d'image. Certains des attributs contenus dans le texte n'apparaissent pas dans l'image générée et l'image générée ressemble à une peinture sans relief et manque de détails. Cet aspect pictural sans relief serait considérablement évident et irrémédiable lors de la génération d'images à plus haute résolution en utilisant les méthodes actuelles. Notre méthode peut produire des images diverses et de haute qualité avec une résolution sans précédent à 1024.

Analyse par calque et évaluation

En général, les calques du générateur à basse résolution contrôlent les styles de haut niveau tels que les lunettes et la pose de la tête. Les calques du milieu contrôlent la coiffure et l'expression faciale, tandis que les calques finaux contrôlent les schémas de couleurs et les détails fins. Nous effectuons une analyse par calque sur le style pré-entraîné que nous avons utilisé dans la plupart des expériences, qui consiste à générer des images de 256 fois 256 et qui comporte 14 calques du vecteur intermédiaire, en nous basant sur les observations empiriques. Nous listons les attributs représentés par les différentes calques d'un style de 14 calques dans le tableau. Les calques de 11 à 14 représentent des micro-caractéristiques ou des structures fines telles que des taches de rousseur ou des pores de la peau, qui peuvent être considérés comme la variation stochastique. Ces variations stochastiques sont particulièrement importantes pour les images haute résolution car elles produisent beaucoup de détails du visage et améliorent la perception visuelle sans affecter les principales structures et attributs de l'image synthétisée.

![image](https://github.com/user-attachments/assets/261629dd-32f5-4805-b583-05a36f7ddb95)


![image](https://github.com/user-attachments/assets/39de1358-952b-4a49-a257-4289bae9586f)

Comparaison.

Nous évaluons notre méthode proposée sur la comparaison de texte et les partitions d'images en la comparant aux approches de AttGAN , ControlGAN , DM-GAN et DF-GAN pour la génération d'images

![image](https://github.com/user-attachments/assets/8f99b8c5-9112-4d2c-8991-78b79b98cd45)

Les flèches ↓ et ↑ à côté de chaque colonne indiquent si l’on cherche à minimiser (↓) ou maximiser (↑) la valeur de la métrique (↓ on veut la plus petite valeure et ↑ on voudra la plus haute valeure ).

![image](https://github.com/user-attachments/assets/b986b09e-c531-431d-b9c9-e03cb7f400ce)

TediGAN a

le FID le plus bas (106,37) ⇒ ses images sont statistiquement les plus proches du réel

le LPIPS le plus bas (0,456) ⇒ ses images ont la meilleure fidélité perçue

la meilleure précision (25,3 %) ⇒ ses images correspondent le plus fidèlement au texte

le meilleur réalisme (31,7 %) ⇒ ses images sont jugées les plus « réelles » par des humains

Explication des parametres:

FID (Fréchet Inception Distance)

Quoi ? Mesure la distance statistique entre la distribution des caractéristiques (features) extraites d’images générées et celle d’images réelles, à l’aide d’un réseau Inception-v3 pré-entraîné.

Pourquoi ? Plus la distance est faible, plus les images synthétiques sont “indiscernables” du vrai jeu de données sur le plan global (textures, formes, couleurs).

Objectif : Minimiser.

LPIPS (Learned Perceptual Image Patch Similarity)

Quoi ? Évalue la similarité perceptuelle locale entre deux images (générée vs. réelle) via un réseau profond entraîné pour refléter la perception humaine.

Pourquoi ? Contrairement à une simple erreur pixel à pixel, LPIPS se concentre sur ce qui « saute aux yeux » (détails, contours, textures).

Objectif : Minimiser.

Accuracy (classification accuracy)

Quoi ? Pourcentage d’images générées correctement reconnues par un classificateur d’attributs (ou de catégories) comme correspondant au texte de commande.

Pourquoi ? Mesure la fidélité sémantique : la capacité du modèle à traduire correctement la description textuelle en contenu visuel.

Objectif : Maximiser.

Realism (réalisme perçu)

Quoi ? Pourcentage d’images que des évaluateurs humains (ou un réseau “discriminateur” entraîné) jugent suffisamment “réelles” pour passer pour de vraies photos.

Pourquoi ? Évalue l’aspect naturel et plausible des visages générés, indépendamment de la correspondance texte.

Objectif : Maximiser.


Comparaison de notre modele avec ManiGAN pour la manipulation d'images avec du texte.

![image](https://github.com/user-attachments/assets/ff13f8a5-b876-4a33-adf3-3c7f95f48ed8)

![image](https://github.com/user-attachments/assets/62371819-a3a8-4ec8-a113-5134fc892950)

Sur CelebA, notre modèle a :

le FID le plus bas (107,25) ⇒ ses images sont statistiquement les plus proches du réel.

la meilleure précision (59,1 %) ⇒ ses images correspondent le plus fidèlement au texte de commande.

le meilleur réalisme (63,8 %) ⇒ ses images sont jugées les plus « réelles » par des humains.

Sur Non-CelebA, notre modèle a :

le FID le plus bas (135,47) ⇒ ses images restent statistiquement plus proches du réel que celles de ManiGAN.

la meilleure précision (87,2 %) ⇒ il traduit la description textuelle en contenu visuel de façon nettement plus fidèle.

le meilleur réalisme (78,3 %) ⇒ il produit les visages les plus naturels et plausibles pour des observateurs humains.


Nous illustrons également la comparaison de l'esquisse (label) à l'image et de l'étiquette (sketch) à la génération d'image.

![image](https://github.com/user-attachments/assets/5faafd2b-4061-4edf-bb31-7d147bf5ca0f)

![image](https://github.com/user-attachments/assets/e06f4ca5-6c67-4b74-8ff2-3562c733a3a9)

Ces résultats expérimentaux démontrent la supériorité de notre méthode en termes d'efficacité de la synthèse d'images, la capacité de générer des résultats de haute qualité et l'extensibilité pour les entrées multimodales.
