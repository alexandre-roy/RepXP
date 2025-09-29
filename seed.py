import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "repxp.settings")
django.setup()

from site_web.models import GroupeMusculaire, Exercice

def run():
    muscular_groups = ["Dos", "Pectoraux", "Épaules", "Avant-bras", "Biceps", "Cardio", "Fessiers", "Jambes", "Triceps"]
    for mc in muscular_groups:
        group = GroupeMusculaire.objects.get_or_create(nom=mc)
        print(f"{group} créé!")

    exercices_data = [
        # DOS
        {
            "nom": "Tirage vertical à la poulie",
            "groupe_musculaire": "Dos",
            "series_sugg": 4,
            "reps_sugg": 10,
            "description": "Assis devant la machine à poulie haute, saisissez la barre en pronation, les mains un peu plus larges que les épaules. Tirez la barre vers le haut de la poitrine en contractant le dos, puis revenez lentement à la position de départ en contrôlant la charge.",
            "image": "images_exercices/lat_pulldown.png",
            "est_approuve": True,
        },
                    {
            "nom": "Tirage vertical à la barre",
            "groupe_musculaire": "Dos",
            "series_sugg": 4,
            "reps_sugg": 10,
            "description": "Saisissez la barre en pronation et tirez votre menton au-dessus de la barre. Gardez le dos droit et contrôlez la descente.",
            "image": "images_exercices/bar_row.png",
            "est_approuve": True,
        },
        {
            "nom": "Tractions à la barre fixe",
            "groupe_musculaire": "Dos",
            "series_sugg": 4,
            "reps_sugg": 10,
            "description": "Saisissez la barre en pronation et tirez votre menton au-dessus de la barre. Gardez le dos droit et contrôlez la descente.",
            "image": "images_exercices/pull_up.png",
            "est_approuve": True,
        },
        {
            "nom": "Rowing barre",
            "groupe_musculaire": "Dos",
            "series_sugg": 4,
            "reps_sugg": 12,
            "description": "Penchez-vous légèrement vers l'avant et tirez la barre vers votre abdomen tout en contractant les omoplates.",
            "image": "images_exercices/bar_row.png",
            "est_approuve": True,
        },
        {
            "nom": "Tirage horizontal à la poulie",
            "groupe_musculaire": "Dos",
            "series_sugg": 3,
            "reps_sugg": 15,
            "description": "Asseyez-vous face à la poulie, tirez la poignée vers votre ventre en gardant le dos droit.",
            "image": "images_exercices/cable_row.png",
            "est_approuve": True,
        },

        # PECTORAUX
        {
            "nom": "Développé couché à la barre",
            "groupe_musculaire": "Pectoraux",
            "series_sugg": 4,
            "reps_sugg": 8,
            "description": "Allongez-vous sur un banc, descendez la barre jusqu'à la poitrine puis poussez-la vers le haut en contractant les pectoraux.",
            "image": "images_exercices/barbel_bench.png",
            "est_approuve": True,
        },
                    {
            "nom": "Développé couché aux haltères",
            "groupe_musculaire": "Pectoraux",
            "series_sugg": 4,
            "reps_sugg": 8,
            "description": "Allongez-vous sur un banc, descendez les haltères jusqu'à la poitrine puis poussez-les vers le haut en contractant les pectoraux.",
            "image": "images_exercices/dumbbell_press.png",
            "est_approuve": True,
        },
        {
            "nom": "Pompes classiques",
            "groupe_musculaire": "Pectoraux",
            "series_sugg": 3,
            "reps_sugg": 20,
            "description": "Placez vos mains au sol à la largeur des épaules et poussez votre corps vers le haut en contractant les pectoraux.",
            "image": "images_exercices/push_up.png",
            "est_approuve": True,
        },
        {
            "nom": "Écarté à la poulie debout",
            "groupe_musculaire": "Pectoraux",
            "series_sugg": 3,
            "reps_sugg": 12,
            "description": "Debout entre deux poulies hautes, saisissez les poignées et ramenez-les lentement l'une vers l'autre devant la poitrine en contractant les pectoraux. Gardez une légère flexion des coudes et contrôlez le mouvement sur toute l’amplitude.",
            "image": "images_exercices/cable_fly.png",
            "est_approuve": True,
        },

        # ÉPAULES
        {
            "nom": "Développé militaire à la barre",
            "groupe_musculaire": "Épaules",
            "series_sugg": 4,
            "reps_sugg": 10,
            "description": "Tenez la barre au niveau des épaules et poussez-la au-dessus de la tête jusqu'à l'extension complète des bras.",
            "image": "images_exercices/military_press_barbel.png",
            "est_approuve": True,
        },
                    {
            "nom": "Développé militaire aux haltères",
            "groupe_musculaire": "Épaules",
            "series_sugg": 4,
            "reps_sugg": 10,
            "description": "Tenez les haltères au niveau des épaules et poussez-les au-dessus de la tête jusqu'à l'extension complète des bras.",
            "image": "images_exercices/military_press_dumbbell.png",
            "est_approuve": True,
        },
        {
            "nom": "Élévations latérales aux haltères",
            "groupe_musculaire": "Épaules",
            "series_sugg": 3,
            "reps_sugg": 15,
            "description": "Tenez un haltère dans chaque main et levez les bras latéralement jusqu'à la hauteur des épaules.",
            "image": "images_exercices/lateral_raise_dumbbell.png",
            "est_approuve": True,
        },
                    {
            "nom": "Élévations latérales à la poulie",
            "groupe_musculaire": "Épaules",
            "series_sugg": 3,
            "reps_sugg": 15,
            "description": "Tenez une poulie dans chaque main et levez les bras latéralement jusqu'à la hauteur des épaules.",
            "image": "images_exercices/cable_lateral_raise.png",
            "est_approuve": True,
        },
        {
            "nom": "Rotation externe à la poulie",
            "groupe_musculaire": "Épaules",
            "series_sugg": 3,
            "reps_sugg": 15,
            "description": "Debout à côté d'une poulie réglée à hauteur du coude, tenez la poignée avec la main extérieure et tirez lentement vers l'extérieur en gardant le coude collé au corps. Contrôlez le retour sans bouger le bras. Exercice idéal pour renforcer la coiffe des rotateurs et stabiliser l'épaule.",
            "image": "images_exercices/shoulder_rotator.png",
            "est_approuve": True,
        },


        # BICEPS
        {
            "nom": "Curl barre droite",
            "groupe_musculaire": "Biceps",
            "series_sugg": 4,
            "reps_sugg": 12,
            "description": "Tenez la barre paumes vers le haut et pliez les coudes pour soulever la barre jusqu'aux épaules.",
            "image": "images_exercices/bicep_bar.png",
            "est_approuve": True,
        },
        {
            "nom": "Curl alterné avec haltères",
            "groupe_musculaire": "Biceps",
            "series_sugg": 3,
            "reps_sugg": 15,
            "description": "Alternez les bras en soulevant les haltères en gardant les coudes près du corps.",
            "image": "images_exercices/bicep_dumbbell.png",
            "est_approuve": True,
        },

        # TRICEPS
        {
            "nom": "Extension triceps à la poulie",
            "groupe_musculaire": "Triceps",
            "series_sugg": 3,
            "reps_sugg": 15,
            "description": "Tirez la corde vers le bas en contractant les triceps jusqu'à l'extension complète des bras.",
            "image": "images_exercices/cable_tricep_pushdown.png",
            "est_approuve": True,
        },
        {
            "nom": "Dips entre deux bancs",
            "groupe_musculaire": "Triceps",
            "series_sugg": 3,
            "reps_sugg": 12,
            "description": "Placez vos mains sur un banc et descendez votre corps en pliant les coudes, puis poussez vers le haut.",
            "image": "images_exercices/dips.png",
            "est_approuve": True,
        },

        # JAMBES
        {
            "nom": "Squat",
            "groupe_musculaire": "Jambes",
            "series_sugg": 4,
            "reps_sugg": 10,
            "description": "Pliez les genoux en gardant le dos droit et poussez sur les talons pour revenir debout.",
            "image": "images_exercices/squat.png",
            "est_approuve": True,
        },
        {
            "nom": "Fentes avant",
            "groupe_musculaire": "Jambes",
            "series_sugg": 3,
            "reps_sugg": 12,
            "description": "Avancez une jambe et descendez jusqu'à former un angle de 90° avec les genoux, puis remontez.",
            "image": "images_exercices/lunge.png",
            "est_approuve": True,
        },
        {
            "nom": "Presse à cuisses",
            "groupe_musculaire": "Jambes",
            "series_sugg": 4,
            "reps_sugg": 10,
            "description": "Poussez la plateforme de la machine avec vos jambes en contrôlant le mouvement à la descente.",
            "image": "images_exercices/leg_press.png",
            "est_approuve": True,
        },

        # FESSIERS
        {
            "nom": "Hip thrust",
            "groupe_musculaire": "Fessiers",
            "series_sugg": 4,
            "reps_sugg": 12,
            "description": "Appuyez le haut du dos sur un banc, poussez les hanches vers le haut en contractant les fessiers.",
            "image": "images_exercices/hip_thrust.png",
            "est_approuve": True,
        },
        # CARDIO
        {
            "nom": "Course sur tapis",
            "groupe_musculaire": "Cardio",
            "series_sugg": 1,
            "reps_sugg": 20,
            "description": "Courez à un rythme modéré sur le tapis pendant plusieurs minutes pour améliorer votre endurance.",
            "image": "images_exercices/treadmill.png",
            "est_approuve": True,
        },
        {
            "nom": "Corde à sauter",
            "groupe_musculaire": "Cardio",
            "series_sugg": 3,
            "reps_sugg": 60,
            "description": "Sautez à la corde à un rythme constant pour stimuler le cardio et la coordination.",
            "image": "images_exercices/rope.png",
            "est_approuve": True,
        },
    ]
    Exercice.objects.all().delete()
    for data in exercices_data:
        groupe = GroupeMusculaire.objects.get(nom=data["groupe_musculaire"])
        exercice = Exercice.objects.get_or_create(
            nom=data["nom"],
            groupe_musculaire_id=groupe.id,
            series_sugg=data["series_sugg"],
            reps_sugg=data["reps_sugg"],
            description=data["description"],
            image=data["image"],
            est_approuve=data["est_approuve"],
        )
        print(f"{exercice} créé!")

if __name__ == "__main__":
    run()