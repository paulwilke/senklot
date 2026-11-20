"""Generate docs/de/ and docs/fr/ from the English page docs/index.html.

python src/i18n.py

Each entry maps an exact English fragment of docs/index.html to its German and
French versions. The script fails loudly if a fragment is missing, so edits to
the English page that need translating are never silently skipped.
Entries whose English starts with "*" are replaced everywhere, others once.
"""
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS = os.path.join(ROOT, "docs")
NB = " "  # French spacing before : ; ? !

S = [
    # ---------------------------------------------------------------- head & nav
    ('<html lang="en">', '<html lang="de">', '<html lang="fr">'),
    ("<title>Senklot · a typeface with a movable centre of mass</title>",
     "<title>Senklot · eine Schrift mit beweglichem Schwerpunkt</title>",
     "<title>Senklot · un caractère au centre de gravité mobile</title>"),
    ('content="Senklot is an original variable sans-serif whose stroke weight follows a movable centre of mass. Roman and italic, 300–800, two ballast axes."',
     'content="Senklot ist eine eigenständige variable Groteske, deren Strichstärke einem beweglichen Schwerpunkt folgt. Aufrecht und kursiv, 300–800, zwei Ballast-Achsen."',
     'content="Senklot est une linéale variable originale dont la graisse suit un centre de gravité mobile. Romain et italique, 300–800, deux axes de lest."'),
    ('content="A sans-serif with a movable centre of mass."',
     'content="Eine Groteske mit beweglichem Schwerpunkt."',
     'content="Une linéale au centre de gravité mobile."'),
    ('*href="fonts/', 'href="../fonts/', 'href="../fonts/'),
    ('*href="downloads/', 'href="../downloads/', 'href="../downloads/'),
    ('<span class="lang"><a href="./" lang="en" aria-current="page">EN</a><a href="de/" lang="de">DE</a><a href="fr/" lang="fr">FR</a></span>',
     '<span class="lang"><a href="../" lang="en">EN</a><a href="./" lang="de" aria-current="page">DE</a><a href="../fr/" lang="fr">FR</a></span>',
     '<span class="lang"><a href="../" lang="en">EN</a><a href="../de/" lang="de">DE</a><a href="./" lang="fr" aria-current="page">FR</a></span>'),
    ('<a href="#play">Playground</a>', '<a href="#play">Ausprobieren</a>', '<a href="#play">Essayer</a>'),
    ('<a href="#italic">Italic</a>', '<a href="#italic">Kursiv</a>', '<a href="#italic">Italique</a>'),
    ('<a href="#glyphs">Glyphs</a>', '<a href="#glyphs">Zeichen</a>', '<a href="#glyphs">Glyphes</a>'),
    ('href="#use">Use</a>', 'href="#use">Einbinden</a>', 'href="#use">Utiliser</a>'),
    ('href="#download">Download</a>', 'href="#download">Download</a>', 'href="#download">Télécharger</a>'),
    ('<a href="#about">Licence</a>', '<a href="#about">Lizenz</a>', '<a href="#about">Licence</a>'),

    # ---------------------------------------------------------------- hero
    ("A sans-serif with a <em>movable centre of mass</em>. Stroke weight depends on where the ink sits, not on which way the stroke runs. Move the weight, and every letter feels it.",
     "Eine Groteske mit <em>beweglichem Schwerpunkt</em>. Die Strichstärke hängt davon ab, wo die Tinte sitzt, nicht davon, in welche Richtung der Strich läuft. Verschiebe das Gewicht, und jeder Buchstabe spürt es.",
     "Une linéale au <em>centre de gravité mobile</em>. La graisse dépend de l’endroit où se trouve l’encre, pas du sens du trait. Déplacez le poids, et chaque lettre le ressent."),
    ("Move your pointer around the title, or scroll quickly to feel its inertia.",
     "Bewege den Zeiger um den Titel oder scrolle schnell, um die Trägheit zu spüren.",
     f"Déplacez le pointeur autour du titre, ou faites défiler rapidement pour sentir son inertie."),
    (">Enable tilt<", ">Neigung aktivieren<", ">Activer l’inclinaison<"),
    (">Download Senklot<", ">Senklot herunterladen<", ">Télécharger Senklot<"),
    ('href="#play">Try it</a>', 'href="#play">Ausprobieren</a>', 'href="#play">Essayer</a>'),

    # ---------------------------------------------------------------- story
    ("<h2>The idea</h2>", "<h2>Die Idee</h2>", "<h2>L’idée</h2>"),
    ("I was on my construction site, working with a plumb bob. Watching it swing, I wondered: what if a typeface could sway and settle like that?",
     "Ich war auf meiner Baustelle und arbeitete mit einem Senklot. Als ich ihm beim Pendeln zusah, fragte ich mich: Was, wenn eine Schrift so schwingen und zur Ruhe kommen könnte?",
     f"J’étais sur mon chantier, un fil à plomb à la main. En le regardant osciller, je me suis demandé{NB}: et si un caractère pouvait se balancer et se poser ainsi{NB}?"),
    ("That’s Senklot.", "Das ist Senklot.", "Voilà Senklot."),
    ("In most fonts, stroke weight follows direction. In Senklot, each letter has a centre of gravity, and you can move it. Sink it, lift it, drift it sideways.",
     "In den meisten Schriften folgt die Strichstärke der Richtung. In Senklot hat jeder Buchstabe einen Schwerpunkt, und du kannst ihn bewegen: absenken, anheben, zur Seite schieben.",
     f"Dans la plupart des caractères, la graisse suit la direction du trait. Dans Senklot, chaque lettre a un centre de gravité que l’on peut déplacer{NB}: le faire descendre, monter, glisser sur le côté."),
    ("The skeleton stays put, so text never reflows. Only the ink moves. The dots and umlauts swing along like loose ballast.",
     "Das Skelett bleibt, wo es ist, also läuft der Text nie um. Nur die Tinte bewegt sich. Punkte und Umlaute schwingen mit wie loser Ballast.",
     "Le squelette ne bouge pas, le texte ne se recompose donc jamais. Seule l’encre se déplace. Les points et les trémas suivent comme un lest libre."),
    ("<i>Senklot</i> is German for plumb bob. Two axes move its weight: <strong>BLSY</strong> up and down, <strong>BLSX</strong> sideways.",
     "Ein <i>Senklot</i> ist das Lot der Bauleute. Zwei Achsen bewegen sein Gewicht: <strong>BLSY</strong> auf und ab, <strong>BLSX</strong> zur Seite.",
     f"<i>Senklot</i> signifie «{NB}fil à plomb{NB}» en allemand. Deux axes déplacent son poids{NB}: <strong>BLSY</strong> vers le haut ou le bas, <strong>BLSX</strong> sur le côté."),

    # ---------------------------------------------------------------- facts
    ("<span>styles: Roman and a true Italic</span>", "<span>Stile: aufrecht und eine echte Kursive</span>", "<span>styles{NB}: romain et une véritable italique</span>".replace("{NB}", NB)),
    ("<span>continuous weight, Light to ExtraBold</span>", "<span>stufenloses Gewicht, Light bis ExtraBold</span>", "<span>graisse continue, de Light à ExtraBold</span>"),
    ("<span>ballast axes no other font has</span>", "<span>Ballast-Achsen, die keine andere Schrift hat</span>", "<span>axes de lest qu’aucun autre caractère ne possède</span>"),
    ("<span>glyphs, Western European Latin</span>", "<span>Zeichen, westeuropäisches Latein</span>", "<span>glyphes, latin d’Europe de l’Ouest</span>"),
    ("The axes combine freely. Bold Italic with the mass sunk to the left is as exact as Regular at rest, because all fifteen masters are interpolated without approximation.",
     "Die Achsen lassen sich frei kombinieren. Bold Italic mit nach links abgesunkener Masse ist genauso exakt wie Regular in Ruhe, weil alle fünfzehn Master ohne Näherung interpoliert werden.",
     "Les axes se combinent librement. Un Bold Italic dont la masse est descendue à gauche est aussi exact qu’un Regular au repos, car les quinze masters sont interpolés sans approximation."),

    # ---------------------------------------------------------------- playground
    ("<h2>Playground</h2>", "<h2>Ausprobieren</h2>", "<h2>Essayer</h2>"),
    ('aria-label="Ballast position"', 'aria-label="Position des Ballasts"', 'aria-label="Position du lest"'),
    ('translateX(-50%)">rises</span>', 'translateX(-50%)">steigt</span>', 'translateX(-50%)">monte</span>'),
    ('translateX(-50%)">sinks</span>', 'translateX(-50%)">sinkt</span>', 'translateX(-50%)">descend</span>'),
    ('translateY(-140%)">left</span>', 'translateY(-140%)">links</span>', 'translateY(-140%)">gauche</span>'),
    ('translateY(-140%)">right</span>', 'translateY(-140%)">rechts</span>', 'translateY(-140%)">droite</span>'),
    ("<span>Weight</span>", "<span>Gewicht</span>", "<span>Graisse</span>"),
    ("<span>Size</span>", "<span>Größe</span>", "<span>Taille</span>"),
    ('*aria-pressed="false">Italic</button>', 'aria-pressed="false">Kursiv</button>', 'aria-pressed="false">Italique</button>'),
    ('id="reset">Reset</button>', 'id="reset">Zurücksetzen</button>', 'id="reset">Réinitialiser</button>'),
    ('id="swing">Swing</button>', 'id="swing">Pendeln</button>', 'id="swing">Balancer</button>'),
    ("Gravity, quietly at work.", "Schwerkraft, leise am Werk.", "La gravité, à l’œuvre en silence."),
    ("*>Copy</button>", ">Kopieren</button>", ">Copier</button>"),

    # ---------------------------------------------------------------- weights & italic
    ("<h2>Six weights · two styles · two files</h2>", "<h2>Sechs Gewichte · zwei Stile · zwei Dateien</h2>", "<h2>Six graisses · deux styles · deux fichiers</h2>"),
    ("<h2>The italic</h2>", "<h2>Die Kursive</h2>", "<h2>L’italique</h2>"),
    ("Senklot Italic is a true italic, not a slanted roman. The skeleton is slanted by 9° <em>before</em> the strokes are drawn, so every stroke keeps its real thickness instead of being squashed.",
     "Senklot Italic ist eine echte Kursive, keine schräg gestellte Aufrechte. Das Skelett wird um 9° geneigt, <em>bevor</em> die Striche gezeichnet werden. So behält jeder Strich seine echte Dicke, statt gestaucht zu werden.",
     "Senklot Italic est une véritable italique, pas un romain penché. Le squelette est incliné de 9° <em>avant</em> que les traits soient tracés, si bien que chaque trait garde sa vraie épaisseur au lieu d’être écrasé."),
    ("Several letters are redrawn. The <em>a</em> becomes single-storey, <em>f</em> drops below the baseline and hooks back, and the stems of <em>a d i h m n u</em> roll out into small exit strokes. The ballast still works: in italic, the mass gathers in those exits.",
     "Mehrere Buchstaben sind neu gezeichnet. Das <em>a</em> wird einstöckig, das <em>f</em> reicht unter die Grundlinie und schwingt zurück, und die Stämme von <em>a d i h m n u</em> laufen in kleine Auslaufstriche aus. Der Ballast funktioniert weiter: In der Kursiven sammelt sich die Masse in diesen Ausläufen.",
     f"Plusieurs lettres sont redessinées. Le <em>a</em> passe à un seul étage, le <em>f</em> descend sous la ligne de base et revient en crochet, et les fûts de <em>a d i h m n u</em> se terminent par de petites sorties. Le lest fonctionne toujours{NB}: en italique, la masse se rassemble dans ces sorties."),
    ("<figcaption>single-storey a</figcaption>", "<figcaption>einstöckiges a</figcaption>", "<figcaption>a à un étage</figcaption>"),
    ("<figcaption>descending f</figcaption>", "<figcaption>f mit Unterlänge</figcaption>", "<figcaption>f descendant</figcaption>"),
    ("*<figcaption>exit stroke</figcaption>", "<figcaption>Auslaufstrich</figcaption>", "<figcaption>trait de sortie</figcaption>"),

    # ---------------------------------------------------------------- states
    ("<h2>Three resting states</h2>", "<h2>Drei Ruhezustände</h2>", "<h2>Trois états de repos</h2>"),
    ("<i>Ruhe</i> (rest). Default. A built-in ballast you sense more than see.",
     "<i>Ruhe</i>. Standard. Ein eingebauter Ballast, den man eher spürt als sieht.",
     "<i>Ruhe</i> (repos). Par défaut. Un lest intégré que l’on sent plus qu’on ne le voit."),
    ("<i>Anker</i> (anchor). BLSY 100. The weight sinks to the baseline like a plumb bob.",
     "<i>Anker</i>. BLSY 100. Das Gewicht sinkt zur Grundlinie wie ein Senklot.",
     "<i>Anker</i> (ancre). BLSY 100. Le poids descend vers la ligne de base comme un fil à plomb."),
    ("<i>Ballon</i> (balloon). BLSY −100. Light underneath, buoyant on top.",
     "<i>Ballon</i>. BLSY −100. Unten leicht, oben voller Auftrieb.",
     "<i>Ballon</i>. BLSY −100. Léger en bas, porté vers le haut."),

    # ---------------------------------------------------------------- text sample
    ("<h2>Text at rest</h2>", "<h2>Text in Ruhe</h2>", "<h2>Le texte au repos</h2>"),
    ("A versatile text typeface has to do two jobs. It must step forward in a headline and step back in a paragraph. At rest, Senklot is a calm, open sans with a generous x-height, wide apertures and squared terminals that snap to the grid.",
     "Eine vielseitige Textschrift hat zwei Aufgaben. In der Überschrift muss sie hervortreten, im Absatz zurücktreten. In Ruhe ist Senklot eine ruhige, offene Groteske mit großzügiger x-Höhe, weiten Öffnungen und gerade abgeschnittenen Strichenden, die auf dem Raster einrasten.",
     "Un caractère de texte polyvalent a deux missions. Il doit s’affirmer dans un titre et s’effacer dans un paragraphe. Au repos, Senklot est une linéale calme et ouverte, avec une hauteur d’x généreuse, des ouvertures larges et des terminaisons droites calées sur la grille."),
    ("Its personality is a slight downward pull: crossbars sit low and stems swell a touch toward the baseline. It is <strong>grounded</strong> without being heavy, and the <em>italic</em> keeps that same quiet weight. Only when you move the mass does the system reveal itself.",
     "Ihr Charakter ist ein leichter Zug nach unten: Querstriche sitzen tief, und Stämme werden zur Grundlinie hin etwas kräftiger. Sie ist <strong>geerdet</strong>, ohne schwer zu sein, und die <em>Kursive</em> behält dieses ruhige Gewicht. Erst wenn du die Masse bewegst, zeigt sich das System.",
     f"Sa personnalité tient à une légère attraction vers le bas{NB}: les barres sont basses et les fûts s’épaississent un peu vers la ligne de base. Elle est <strong>ancrée</strong> sans être lourde, et l’<em>italique</em> garde ce même poids tranquille. Ce n’est qu’en déplaçant la masse que le système se révèle."),
    ("Größe, Übermut und Äpfel: the umlauts carry their own ballast. The figures 0123456789 stand on the same plumb line.",
     "Größe, Übermut und Äpfel: Die Umlaute tragen ihren eigenen Ballast. Die Ziffern 0123456789 stehen im selben Lot.",
     f"Größe, Übermut und Äpfel{NB}: les trémas portent leur propre lest. Les chiffres 0123456789 tiennent le même aplomb."),
    ("<em>Built from a parametric stroke skeleton. Every outline is original geometry; nothing is traced or derived from an existing font.</em>",
     "<em>Aufgebaut aus einem parametrischen Strichskelett. Jede Kontur ist eigene Geometrie; nichts ist von einer bestehenden Schrift nachgezeichnet oder abgeleitet.</em>",
     f"<em>Construit à partir d’un squelette de traits paramétrique. Chaque contour est une géométrie originale{NB}; rien n’est décalqué ni dérivé d’un caractère existant.</em>"),

    # ---------------------------------------------------------------- glyphs & axes
    ("<h2>Character set · hover, tap or tab to a glyph</h2>",
     "<h2>Zeichensatz · Zeichen antippen, mit der Maus berühren oder per Tab ansteuern</h2>",
     "<h2>Jeu de caractères · survolez, touchez ou atteignez un glyphe avec Tab</h2>"),
    ("<h2>Axes</h2>", "<h2>Achsen</h2>", "<h2>Axes</h2>"),
    ("<th>Axis</th><th>Range</th><th>Default</th><th>What it does</th><th>How to set it</th>",
     "<th>Achse</th><th>Bereich</th><th>Standard</th><th>Wirkung</th><th>Einstellen mit</th>",
     "<th>Axe</th><th>Plage</th><th>Défaut</th><th>Effet</th><th>Réglage</th>"),
    ("Light to ExtraBold. Spacing opens up as strokes get heavier.",
     "Light bis ExtraBold. Mit kräftigeren Strichen wird auch der Abstand weiter.",
     "De Light à ExtraBold. L’approche s’élargit à mesure que les traits s’épaississent."),
    ("Mass rises (−) or sinks toward the baseline (+). Positive pulls down, like a plumb line and like screen coordinates.",
     "Masse steigt (−) oder sinkt zur Grundlinie (+). Positiv zieht nach unten, wie ein Lot und wie Bildschirmkoordinaten.",
     "La masse monte (−) ou descend vers la ligne de base (+). Le positif tire vers le bas, comme un fil à plomb et comme les coordonnées d’écran."),
    ("Mass drifts left (−) or right (+).", "Masse wandert nach links (−) oder rechts (+).", "La masse glisse à gauche (−) ou à droite (+)."),
    ("<tr><td>Italic</td><td>Roman / Italic</td><td>Roman</td><td>Separate file, picked automatically.</td>",
     "<tr><td>Kursiv</td><td>Aufrecht / Kursiv</td><td>Aufrecht</td><td>Eigene Datei, wird automatisch gewählt.</td>",
     "<tr><td>Italique</td><td>Romain / Italique</td><td>Romain</td><td>Fichier séparé, choisi automatiquement.</td>"),
    ("The ballast axes never change advance widths, so you can animate them on running text without any reflow. The weight axis does change widths, as weight axes in every family do.",
     "Die Ballast-Achsen ändern nie die Laufweiten. Du kannst sie also in Fließtext animieren, ohne dass etwas umbricht. Die Gewichtsachse ändert die Breiten, wie Gewichtsachsen in jeder Schriftfamilie.",
     "Les axes de lest ne modifient jamais les chasses, on peut donc les animer dans un texte courant sans recomposition. L’axe de graisse, lui, modifie les chasses, comme dans toute famille."),

    # ---------------------------------------------------------------- use
    ("<h2>Use it on your site</h2>", "<h2>Auf deiner Website einbinden</h2>", "<h2>L’utiliser sur votre site</h2>"),
    ("<h3>Copy the files</h3>", "<h3>Dateien kopieren</h3>", "<h3>Copier les fichiers</h3>"),
    ("Unzip the download and copy the contents of <code>web/</code> into a folder on your site, for example <code>/fonts/</code>. You need <code>senklot.css</code>, the two variable <code>.woff2</code> files and <code>OFL.txt</code>, which keeps the licence with the fonts.",
     "Entpacke den Download und kopiere den Inhalt von <code>web/</code> in einen Ordner deiner Website, zum Beispiel <code>/fonts/</code>. Du brauchst <code>senklot.css</code>, die beiden variablen <code>.woff2</code>-Dateien und <code>OFL.txt</code>, damit die Lizenz bei den Schriften bleibt.",
     "Décompressez le téléchargement et copiez le contenu de <code>web/</code> dans un dossier de votre site, par exemple <code>/fonts/</code>. Il vous faut <code>senklot.css</code>, les deux fichiers variables <code>.woff2</code> et <code>OFL.txt</code>, qui garde la licence avec les fontes."),
    ("<h3>Link the stylesheet</h3>", "<h3>Stylesheet einbinden</h3>", "<h3>Lier la feuille de style</h3>"),
    ("<h3>Use it like any font</h3>", "<h3>Wie jede Schrift verwenden</h3>", "<h3>L’utiliser comme n’importe quelle fonte</h3>"),
    ("<h3>Move the ballast</h3>", "<h3>Den Ballast bewegen</h3>", "<h3>Déplacer le lest</h3>"),
    ("Weight and italic use normal CSS. The ballast axes go through <code>font-variation-settings</code>. That property replaces itself as a whole, so always set both axes together. Custom properties make that easy:",
     "Gewicht und Kursive funktionieren mit normalem CSS. Die Ballast-Achsen laufen über <code>font-variation-settings</code>. Diese Eigenschaft wird immer als Ganzes ersetzt, setze also beide Achsen zusammen. Mit Custom Properties geht das einfach:",
     f"La graisse et l’italique passent par le CSS habituel. Les axes de lest passent par <code>font-variation-settings</code>. Cette propriété se remplace en bloc{NB}: définissez donc toujours les deux axes ensemble. Les propriétés personnalisées simplifient cela{NB}:"),
    ("<h3>Animate from JavaScript</h3>", "<h3>Mit JavaScript animieren</h3>", "<h3>Animer en JavaScript</h3>"),
    ("This drives the custom properties from step 4, so the CSS there stays in charge and reduced motion is respected.",
     "Das steuert die Custom Properties aus Schritt 4. So behält das CSS dort die Kontrolle, und reduzierte Bewegung wird respektiert.",
     "Ce code pilote les propriétés personnalisées de l’étape 4. Le CSS garde ainsi la main et la réduction des animations est respectée."),
    ("Browser support: variable fonts with custom axes work in all current versions of Chrome, Edge, Safari and Firefox. For legacy browsers or environments without variable font support, the static files in <code>web/static/</code> give six fixed weights per style without the ballast axes.",
     "Browser-Unterstützung: Variable Fonts mit eigenen Achsen funktionieren in allen aktuellen Versionen von Chrome, Edge, Safari und Firefox. Für ältere Browser oder Umgebungen ohne Variable Fonts bieten die statischen Dateien in <code>web/static/</code> sechs feste Gewichte pro Stil, ohne Ballast-Achsen.",
     f"Compatibilité{NB}: les fontes variables à axes personnalisés fonctionnent dans toutes les versions actuelles de Chrome, Edge, Safari et Firefox. Pour les anciens navigateurs ou les environnements sans fontes variables, les fichiers statiques de <code>web/static/</code> offrent six graisses fixes par style, sans les axes de lest."),

    # ---------------------------------------------------------------- download
    ("<h2>Download</h2>", "<h2>Download</h2>", "<h2>Téléchargement</h2>"),
    ("Everything: web fonts, variable TTFs for desktop apps, 12 static instances, the README and the licence.",
     "Alles drin: Webfonts, variable TTFs für Desktop-Programme, 12 statische Schnitte, das README und die Lizenz.",
     f"Tout y est{NB}: fontes web, TTF variables pour les applications de bureau, 12 instances statiques, le README et la licence."),
    ("<span>Roman · 72 KB</span>", "<span>Aufrecht · 72 KB</span>", "<span>Romain · 72 Ko</span>"),
    ("<span>Italic · 80 KB</span>", "<span>Kursiv · 80 KB</span>", "<span>Italique · 80 Ko</span>"),
    ("<span>@font-face, ready to use</span>", "<span>@font-face, sofort einsatzbereit</span>", "<span>@font-face, prêt à l’emploi</span>"),
    ("<span>desktop apps, in the zip</span>", "<span>Desktop-Programme, im Zip</span>", "<span>applications de bureau, dans le zip</span>"),
    ("<span>12 × TTF and WOFF2, ≈10 KB each</span>", "<span>12 × TTF und WOFF2, je ≈10 KB</span>", "<span>12 × TTF et WOFF2, ≈10 Ko chacun</span>"),

    # ---------------------------------------------------------------- how
    ("<h2>How it is made</h2>", "<h2>Wie sie entsteht</h2>", "<h2>Comment il est construit</h2>"),
    ("Every glyph is a skeleton of straight lines and superellipse arcs. The outline is drawn by offsetting each point of that skeleton by a half-width taken from the field:",
     "Jedes Zeichen ist ein Skelett aus Geraden und Superellipsen-Bögen. Die Kontur entsteht, indem jeder Punkt dieses Skeletts um eine halbe Strichbreite aus dem Feld versetzt wird:",
     f"Chaque glyphe est un squelette de droites et d’arcs de superellipse. Le contour est obtenu en décalant chaque point de ce squelette d’une demi-épaisseur tirée du champ{NB}:"),
    ("half-width = base × contrast × (1 + 0.10·v + 0.55·BLSY·v + 0.40·BLSX·u)",
     "halbe Breite = Basis × Kontrast × (1 + 0.10·v + 0.55·BLSY·v + 0.40·BLSX·u)",
     "demi-épaisseur = base × contraste × (1 + 0.10·v + 0.55·BLSY·v + 0.40·BLSX·u)"),
    ("Here <code>u</code> is the horizontal position from the centre of the letter (−1 left to +1 right) and <code>v</code> the height, running from +1 at the descender to about −0.7 at the ascender. <code>BLSY</code> and <code>BLSX</code> are the axis values divided by 100, so −1 to +1. Because every outline point depends linearly on that half-width, the font interpolates exactly between its masters.",
     "Dabei ist <code>u</code> die waagerechte Position ab der Buchstabenmitte (−1 links bis +1 rechts) und <code>v</code> die Höhe, von +1 an der Unterlänge bis etwa −0,7 an der Oberlänge. <code>BLSY</code> und <code>BLSX</code> sind die Achsenwerte geteilt durch 100, also −1 bis +1. Weil jeder Konturpunkt linear von dieser halben Breite abhängt, interpoliert die Schrift exakt zwischen ihren Mastern.",
     "Ici, <code>u</code> est la position horizontale depuis le centre de la lettre (−1 à gauche, +1 à droite) et <code>v</code> la hauteur, de +1 au jambage inférieur à environ −0,7 au jambage supérieur. <code>BLSY</code> et <code>BLSX</code> sont les valeurs des axes divisées par 100, donc de −1 à +1. Comme chaque point du contour dépend linéairement de cette demi-épaisseur, la fonte s’interpole exactement entre ses masters."),
    ("15 masters per style, including corners for weight × ballast, so combinations stay exact.",
     "15 Master pro Stil, inklusive Ecken für Gewicht × Ballast, damit Kombinationen exakt bleiben.",
     "15 masters par style, y compris les coins graisse × lest, pour que les combinaisons restent exactes."),
    ("As weight increases, round edges are pulled inward so overshoots stay on the guidelines.",
     "Mit steigendem Gewicht werden runde Kanten nach innen gezogen, damit Überhänge auf den Hilfslinien bleiben.",
     "Quand la graisse augmente, les bords arrondis sont ramenés vers l’intérieur pour que les débordements restent sur les lignes de référence."),
    ("The italic shears the skeleton by 9° before stroking, so strokes keep their perpendicular thickness.",
     "Die Kursive neigt das Skelett um 9°, bevor die Striche entstehen, damit sie ihre senkrechte Dicke behalten.",
     "L’italique incline le squelette de 9° avant le tracé, si bien que les traits gardent leur épaisseur perpendiculaire."),
    ("Class kerning for the usual pairs, including the accented letters.",
     "Klassen-Kerning für die üblichen Paare, auch für Buchstaben mit Akzent.",
     "Crénage par classes pour les paires courantes, lettres accentuées comprises."),
    ("All files pass the OpenType Sanitizer, the check browsers run on web fonts.",
     "Alle Dateien bestehen den OpenType Sanitizer, die Prüfung, die Browser bei Webfonts durchführen.",
     "Tous les fichiers passent l’OpenType Sanitizer, le contrôle que les navigateurs appliquent aux fontes web."),

    # ---------------------------------------------------------------- licence
    ("<h2>Licence, provenance, limits</h2>", "<h2>Lizenz, Herkunft, Grenzen</h2>", "<h2>Licence, provenance, limites</h2>"),
    ("<h3>Provenance</h3>", "<h3>Herkunft</h3>", "<h3>Provenance</h3>"),
    ("Senklot was generated from original parametric skeletons written for this project. No outlines, metrics or data from any existing font were used, traced or derived.",
     "Senklot wurde aus eigenen parametrischen Skeletten erzeugt, die für dieses Projekt geschrieben wurden. Es wurden keine Konturen, Metriken oder Daten einer bestehenden Schrift verwendet, nachgezeichnet oder abgeleitet.",
     "Senklot a été généré à partir de squelettes paramétriques originaux écrits pour ce projet. Aucun contour, aucune métrique ni aucune donnée d’un caractère existant n’a été utilisé, décalqué ou dérivé."),
    ('<h3 style="margin-top:28px">Licence</h3>', '<h3 style="margin-top:28px">Lizenz</h3>', '<h3 style="margin-top:28px">Licence</h3>'),
    ('Senklot is free and open under the <a href="https://openfontlicense.org">SIL Open Font License 1.1</a>. Use it on websites, in apps, print and commercial work, embed it, modify it and share it. The key conditions, in short:',
     'Senklot ist frei und offen unter der <a href="https://openfontlicense.org">SIL Open Font License 1.1</a>. Du darfst sie auf Websites, in Apps, im Druck und für kommerzielle Arbeiten nutzen, einbetten, verändern und weitergeben. Die wichtigsten Bedingungen in Kürze:',
     f'Senklot est libre et ouvert sous la <a href="https://openfontlicense.org">SIL Open Font License 1.1</a>. Vous pouvez l’utiliser sur des sites, dans des applications, en impression et pour des travaux commerciaux, l’incorporer, le modifier et le partager. Les conditions essentielles, en bref{NB}:'),
    ("Don't sell the font files on their own. Selling a product that uses or bundles them is fine.",
     "Die Schriftdateien dürfen nicht für sich allein verkauft werden. Ein Produkt zu verkaufen, das sie nutzt oder mitliefert, ist erlaubt.",
     "Ne vendez pas les fichiers de fontes seuls. Vendre un produit qui les utilise ou les inclut est autorisé."),
    ("When you pass the font files on, for example in a theme, an app or a download, include the copyright notice and the licence (<code>OFL.txt</code>). Using them on a website you run only needs the files on your server; the licence comes along in <code>web/</code>.",
     "Wer die Schriftdateien weitergibt, zum Beispiel in einem Theme, einer App oder einem Download, muss den Copyright-Hinweis und die Lizenz (<code>OFL.txt</code>) beilegen. Für die Nutzung auf deiner eigenen Website reichen die Dateien auf deinem Server; die Lizenz liegt in <code>web/</code> schon dabei.",
     f"Si vous redistribuez les fichiers, par exemple dans un thème, une application ou un téléchargement, joignez la mention de copyright et la licence (<code>OFL.txt</code>). Pour un usage sur votre propre site, il suffit de placer les fichiers sur votre serveur{NB}; la licence est déjà incluse dans <code>web/</code>."),
    ("Modified versions must stay under the OFL and must not be called “Senklot”, which is a Reserved Font Name.",
     "Veränderte Versionen müssen unter der OFL bleiben und dürfen nicht „Senklot“ heißen. Senklot ist ein reservierter Schriftname (Reserved Font Name).",
     f"Les versions modifiées doivent rester sous OFL et ne peuvent pas s’appeler «{NB}Senklot{NB}», qui est un nom de fonte réservé (Reserved Font Name)."),
    ('This summary is for orientation only. The <a href="https://github.com/paulwilke/senklot/blob/main/OFL.txt">full licence text</a> is what applies. The website and build code are under the <a href="https://github.com/paulwilke/senklot/blob/main/src/LICENSE.txt">MIT licence</a>.',
     'Diese Zusammenfassung dient nur der Orientierung. Rechtlich gilt der <a href="https://github.com/paulwilke/senklot/blob/main/OFL.txt">vollständige englische Lizenztext</a>. Website und Build-Code stehen unter der <a href="https://github.com/paulwilke/senklot/blob/main/src/LICENSE.txt">MIT-Lizenz</a>.',
     'Ce résumé n’est donné qu’à titre indicatif. Seul le <a href="https://github.com/paulwilke/senklot/blob/main/OFL.txt">texte intégral de la licence</a>, en anglais, fait foi. Le site et le code de génération sont sous <a href="https://github.com/paulwilke/senklot/blob/main/src/LICENSE.txt">licence MIT</a>.'),
    ("<h3>Known limits</h3>", "<h3>Bekannte Grenzen</h3>", "<h3>Limites connues</h3>"),
    ("No TrueType hinting, so small sizes on Windows look slightly softer. macOS, iOS and Android are unaffected.",
     "Kein TrueType-Hinting, daher wirken kleine Größen unter Windows etwas weicher. macOS, iOS und Android sind nicht betroffen.",
     "Pas de hinting TrueType{NB}: les petites tailles paraissent un peu plus douces sous Windows. macOS, iOS et Android ne sont pas concernés.".replace("{NB}", NB)),
    ("No small caps, ligatures or alternate figures yet.",
     "Noch keine Kapitälchen, Ligaturen oder alternativen Ziffern.",
     "Pas encore de petites capitales, de ligatures ni de chiffres alternatifs."),
    ("Western European Latin only. Polish, Czech and other Central European letters are missing.",
     "Nur westeuropäisches Latein. Polnische, tschechische und andere mitteleuropäische Buchstaben fehlen.",
     "Latin d’Europe de l’Ouest uniquement. Les lettres polonaises, tchèques et d’Europe centrale manquent."),
    (">Source on GitHub</a>", ">Quellcode auf GitHub</a>", ">Code source sur GitHub</a>"),
    ('<a href="legal/#en">Legal notice &amp; privacy</a>', '<a href="../legal/#de">Impressum &amp; Datenschutz</a>',
     '<a href="../legal/#fr">Mentions légales &amp; confidentialité</a>'),
    (">Theme: auto</button>", ">Design: auto</button>", ">Thème : auto</button>".replace(" :", NB + ":")),

    # ---------------------------------------------------------------- script strings
    ("const T = { copy: 'Copy', copied: 'Copied', select: 'Select & copy', theme: 'Theme', auto: 'auto', light: 'light', dark: 'dark', reduced: 'Reduced motion is on, so the headline stays at rest. Try the playground below.' };",
     "const T = { copy: 'Kopieren', copied: 'Kopiert', select: 'Markieren & kopieren', theme: 'Design', auto: 'auto', light: 'hell', dark: 'dunkel', reduced: 'Reduzierte Bewegung ist aktiv, deshalb bleibt die Überschrift ruhig. Probiere es weiter unten aus.' };",
     "const T = { copy: 'Copier', copied: 'Copié', select: 'Sélectionner et copier', theme: 'Thème', auto: 'auto', light: 'clair', dark: 'sombre', reduced: 'La réduction des animations est activée, le titre reste donc immobile. Essayez plus bas.' };"),
]


def main():
    src = open(os.path.join(DOCS, "index.html"), encoding="utf-8").read()
    for col, lang in ((1, "de"), (2, "fr")):
        s = src
        for row in S:
            en, tr = row[0], row[col]
            every = en.startswith("*")
            en = en.lstrip("*")
            assert en in s, f"[{lang}] fragment not found: {en[:80]}"
            s = s.replace(en, tr) if every else s.replace(en, tr, 1)
        if lang == "fr":
            s = s.replace("tbtn.textContent = T.theme + ': ' + T[mode];", f"tbtn.textContent = T.theme + '{NB}: ' + T[mode];")
        os.makedirs(os.path.join(DOCS, lang), exist_ok=True)
        open(os.path.join(DOCS, lang, "index.html"), "w", encoding="utf-8").write(s)
        print("wrote", lang)


if __name__ == "__main__":
    main()
