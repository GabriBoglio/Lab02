def carica_da_file(file_path):
    album = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            linee = f.readlines()


            if not linee:
                return album


            for linea in linee[1:]:
                linea = linea.strip()
                if not linea:
                    continue

                parti = linea.split(",")
                if len(parti) == 5:
                    codice = parti[0].strip()
                    titolo = parti[1].strip()
                    autore = parti[2].strip()
                    mese = int(parti[3].strip())
                    anno = int(parti[4].strip())

                    foto = {
                        "codice": codice,
                        "titolo": titolo,
                        "autore": autore,
                        "mese": mese,
                        "anno": anno
                    }


                    anno_trovato = False
                    for gruppo in album:
                        if gruppo["anno"] == anno:
                            gruppo["foto"].append(foto)
                            anno_trovato = True
                            break


                    if not anno_trovato:
                        album.append({"anno": anno, "foto": [foto]})

        return album
    except FileNotFoundError:
        return None


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):

    if mese < 1 or mese > 12:
        return None


    for gruppo in album:
        for f in gruppo["foto"]:
            if f["codice"] == codice:
                return None

    nuova_foto = {
        "codice": codice,
        "titolo": titolo,
        "autore": autore,
        "mese": mese,
        "anno": anno
    }


    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"{codice},{titolo},{autore},{mese},{anno}\n")
    except FileNotFoundError:
        return None


    anno_trovato = False
    for gruppo in album:
        if gruppo["anno"] == anno:
            gruppo["foto"].append(nuova_foto)
            anno_trovato = True
            break

    if not anno_trovato:
        album.append({"anno": anno, "foto": [nuova_foto]})

    return nuova_foto


def cerca_foto(album, codice):

    for gruppo in album:
        for f in gruppo["foto"]:
            if f["codice"] == codice:
                return f"{f['codice']}, {f['titolo']}, {f['autore']}, {f['mese']}, {f['anno']}"
    return None


def elenco_foto_anno_per_titolo(album, anno):

    for gruppo in album:
        if gruppo["anno"] == anno:

            titoli = [f["titolo"] for f in gruppo["foto"]]
            return sorted(titoli)


    return None


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    print("Album caricato con successo.")
                    break
                else:
                    print("Errore: File non trovato. Riprova.")

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto (codice duplicato, mese non valido o file mancante).")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
