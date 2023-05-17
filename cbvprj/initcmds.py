from iscrizioni.models import Studente, Insegnamento

def erase_db():
    print("muori db!")
    Studente.objects.all().delete()
    Insegnamento.objects.all().delete()


def init_db():

    if Studente.objects.all().count() > 0:
        return

    lista_studenti = [
        ("Mario", "Bianchi"),
        ("Giorgio", "Rame"),
        ("Mike", "Hermantraut"),
        ("Saul", "Goodman"),
        ("Mike", "Wasoski")
    ]

    lista_insegnamenti = [
        "Difesa dalle arti oscure",
        "Tecnologie Web",
        "Charge Blade Tutorial 101",
        "Kassadin flaming",
        "How to be a PDF by jax"
    ]

    for s in lista_studenti:
        s_db = Studente()
        s_db.name = s[0]
        s_db.surname = s[1]
        s_db.save()


    studenti = Studente.objects.all()

    for index, ins in enumerate(lista_insegnamenti):
        ins_db = Insegnamento()
        ins_db.titolo = ins
        ins_db.save()

        if index == 0: continue
        count = 0
        for s in studenti:
            ins_db.studenti.add(s)
            count += 1
            if count > index:
                break

    print("DUMP BP")
    print("Studenti")
    for s in studenti:
        print(s)

    print("Insegnamenti")
    for i in Insegnamento.objects.all():
        print(i)
        print("Studenti iscritti " + str(i.studenti.all()))
