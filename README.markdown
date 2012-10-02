#Dokumentation

##ADMIN
användarnamn leon  
lösenord leon

##SETUP
Projektet använder django 1.4, twitter bootstrap och en django implementation av twitter bootstrap formulär som kallas django bootstrap.
Databasen som används är SqLite3. för den givna databasen är användarnamn och lösenord leon.
Sidan körs igång med kommandot:  
    python manage.py runserver 0.0.0.0:8000
innifrån mappen inlupp 

##INLEDNING
Mitt projekt heter TimeForTale och går ut på att användare ska kunna skriva berättelser tillsammans.
Detta görs genom att man skriver meddelanden av begränsad längd i en ordnad följd.

Jag har dessutom använt en template context processor som heter request (django.core.context_processors.request) vilken gör requestobjekt tillgängliga i templates. Detta för att göra det möjligt att lägga till en egen templatetag (inlupp.app.templatetags.tags). Den används sedan i base.html för att baserat på sökvägen ange vilken menyflik som är aktiv.

Alla mina templates ligger i inlupp.app.templates och alla ärver utav base.html utom newsnippet.html som ärver av story.html.

Jag hade den fiffiga idén att låta användarna ge en beskrivning på max 80 tecken vilken sedan skulle linewrappas utan hänsyn till ord och agera som avatar. Eftersom sidan kretsar kring texter kändes detta passande till temat. 

##STRUKTUR/TEMPLATES
Sidan består av:
    *För icke inloggade:
        *Loginsida(login.html): 
            logga in & länk till skapa konto
        *Skapa konto sida(register.html): 
            skapa konto och loggas in
    *För inloggade användare:
        *Home(home.html): 
            Visar de senaste listorna, länkar till berättelser och deras skapares 
        *enskilda berättelser(story.html):
            nås via länkar från home. Här postas textstyckena som utgör berättelserna och länkar finns till de olika författarnas profilsidor.
        *Skapa berättelse:
        *Vänner(friends.html):
            länkar till alla vänners användarprofiler
        *Profil(profile.html):
            användarens beskrivning och namn
        *Utloggning:
            förstör sessionen och skickar tillbaka användaren till login.
    *För administratörer:
        -djangos.contrib.admin, djangos inbyggda admin gränssnitt.


#MODELLER:

django.contrib.auth.models.User:
    djangos inbyggda User klass

UserProfile:
    utbyggnad av userklassen som endast innehåller en främmande nyckel till User och en beskrivning på max 80 tecken.
    Dess unicode metod skriver ut beskrivningen på åtta rader med tio tecken. Ifall beskrivningen är kortare än 80 tecken så fylls resten upp.

Story
    Har en titel, främmande nyckel till användaren som skrivit den, datumfält och fyra valbara: 
        -tillgänglighet, vilken inte används än men ska avgöra vilka som ska kunna se och göra tillägg . till berättelsen. I alpha releasen är alla berättelser public. 
        -kategorier
        -språk
        -längd på berättelsen i antal bokstäver

Snippet
    Ett textstycke, främmande nyckel till story och författare, datum och själva texten.

Friendship
    Innehåller datum när vänskapsrelationen skapades och främmande nyckel till de båda parterna.

Alla fyra modeller har en varsin admin.ModelAdmin klass för att göra dem tillgängliga i admin gränssnittet.


#FORMS:

Vanliga forms:
    LoginForm:
        Tar namn och lösenord.
    RegForm
        Tar namn, lösenord, bekräftelse av lösenordet och en beskrivning av användaren.
ModelForm - skapas automatiskt baserat på en modell
    SnippetForm:
        Bygger på snippetmodellen men utesluter fälten för främmande nycklar till användare och berättelse, vilka läggs till baserat på vem som är inloggad och vilken berättelse den är på. Räknaren som håller reda på ordningen av inläggen utesluts också och uppdateras istället vid request. Denna är tänkta att fungera som ett lås så att två tillägg inte kan postas till samma berättelse samtidigt.
    StoryForm:
        Ùtesluter endast främmandenyckel till skaparen.

Friendship modellen behövde inget formulär då all data som behövs är tillgänglig i requestet.

#SAMMANFATTNING

De saker jag gjort som jag anser ligger utanför kursens innehåll (i enlighet med betygskriterier) är:
    -användning av twitter bootstrap och django bootstrap. Användning av CSS var förövrigt meckigare än väntat i django.
    -implementationen av egen template tag för att reda ut vissa av dessa svårigheter.
