#!/usr/bin/env python3
"""Tantric Prayer — Thirty-Six Prayers for the Inner Weather.
9 navarasas x 4 prayers, same spread format as Practical Prayers.
Rasa theory from Abhinavabhāratī/Tantrāloka (house LOGICVID sessions).
Run with the patala venv python (indic_transliteration)."""

import json, html, pathlib

HERE = pathlib.Path(__file__).parent
try:
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate as _tr
except Exception:
    _tr = None

META = dict(
    title="Tantric Prayer",
    subtitle="Thirty-Six Prayers for the Inner Weather",
    blurb="the nine rasas · four prayers each · kashmir shaivism",
    epi_iast="api labdhabhavadbhāvaḥ svātmollāsamayaṃ jagat / paśyan bhaktirasābhogair bhaveyam aviyojitaḥ",
    epi_en="seeing the world as the delight of the self — may i never be parted from it, through the enjoyment of devotion's rasa.",
    epi_src="Utpaladeva, Śivastotrāvalī 5.16",
)

# rasa doctrine line printed under each section divider (sthāyin + Abhinava principle)
DOCTRINE = {
 "srgara": "sthāyin: rati — the beloved becomes the light of consciousness; separation is its fuel (Abhinavabhāratī)",
 "hasa": "sthāyin: hāsa — the world-as-joke; laughter is the register of the play seen from inside",
 "karuna": "sthāyin: śoka — “all rasas are essentially pleasurable, even the painful” — grief is bliss in a minor key (Abhinavabhāratī)",
 "raudra": "sthāyin: krodha — anger exists because it is one with the wonder that is the experience of consciousness (Tantrāloka 15254)",
 "vira": "sthāyin: utsāha — enthusiasm is the energy of recognition, not of the task",
 "bhayanaka": "sthāyin: bhaya — fear is real even when its object is a rope; use the realness, skip the object (Abhinavabhāratī, rope-snake)",
 "bibhatsa": "sthāyin: jugupsā — disgust points at the un-looked-at; the cure is darśana, seeing",
 "adbhuta": "sthāyin: vismaya — wonder (camatkāra) is the primary characteristic of consciousness itself (Tantrāloka ad 1/53)",
 "santa": "sthāyin: śānti — the ninth rasa, Abhinavagupta's own addition: the ocean in which the other eight swim",
}


# three-layer naming: literal Sanskrit gloss + conventional rasa term (MW-standard English)
GLOSS = {
 "srgara": "śṛṅgāra — \"amorous sentiment, love; the beauty that adorns\" (Monier-Williams)",
 "hasa": "hāsya — \"laughable, comic; mockery — that which slays\" (from hās, to slay)",
 "karuna": "karuṇā — \"compassion, mercy; the pitiable, what moves to pity\"",
 "raudra": "raudra — \"furious, stormy — the mood of Rudra\" (rudra: to roar)",
 "vira": "vīra — \"heroic, manly valour; mighty effort\"",
 "bhayanaka": "bhayānaka — \"causing fear: terrible, dreadful\" (bhaya: fear)",
 "bibhatsa": "bībhatsa — \"loathsome, revolting; that which excites disgust\"",
 "adbhuta": "adbhuta — \"the un-become: astonishing, marvellous, unprecedented\" (a-dbhūta)",
 "santa": "śānta — \"pacified, allayed, put to rest\" — the ninth, added by Abhinavagupta",
}

SECTIONS = [
    ("srgara", "I", "Śṛṅgāra", "the Erotic — desire & longing"),
    ("hasa", "II", "Hāsya", "the Comic — mirth & laughter"),
    ("karuna", "III", "Karuṇā", "the Pathetic — grief & compassion"),
    ("raudra", "IV", "Raudra", "the Furious — anger & rage"),
    ("vira", "V", "Vīra", "the Heroic — valour & energy"),
    ("bhayanaka", "VI", "Bhayānaka", "the Horrible — fear & anxiety"),
    ("bibhatsa", "VII", "Bībhatsa", "the Disgusting — disgust & self-loathing"),
    ("adbhuta", "VIII", "Adbhuta", "the Marvellous — wonder & awe"),
    ("santa", "IX", "Śānta", "the Peaceful — Abhinavagupta's ninth"),
]

E = [
# ---------------- I. ŚṚṄGĀRA ----------------
dict(id="srg-1", section="srgara", title="The Un-Drunk One's Thirst", corpus=[1,11],
 source="Utpaladeva, Śivastotrāvalī 1.11",
 en="may the higher knowledge come from tasting the nectar of your devotion —\nthat state, lord, turn toward me,\nkeen as the not-yet-drunk one's thirst for the first drink.",
 brief="Desire as holy thirst — rati aimed at God instead of at the world.",
 logic="The sthāyin rati is not to be removed but redirected. The verse names the exact texture: nāsavas-śuktatā, the eagerness of one who has NOT yet tasted — the pre-taste longing. Knowledge itself (bodha) comes by the sip; the prayer is therefore for the thirst to be aimed at him, and for the state to turn toward the speaker.",
 howto="When longing is loud: say the verse and let the object of the longing become the taste of devotion rather than the thing you'd grab. Feeling-tip: keep the ache — it is the rasa before it arrives; the thirst IS the practice.",
 source_path="sources/sivastotravali_corpus.json", source_ref="1.11"),
dict(id="srg-2", section="srgara", title="The Wine of Non-Difference", corpus=[4,18],
 source="Utpaladeva, Śivastotrāvalī 4.18",
 en="let me not spend one moment here as anything\nother than your servant's vessel — one who reverently,\nunceasingly drinks the rasa-wine of your non-difference.",
 brief="Devotion as intoxication: the wine is non-duality itself.",
 logic="Abheda-rasāsava — the wine of non-difference. Śṛṅgāra's whole lexicon (wine, tasting, the beloved's feet) is applied to the doctrine: the beloved is not other, and the intoxication is the insight. The sthāyin rati becomes the taste of the one, and the servant becomes the vessel that holds it.",
 howto="When you crave closeness to something: say it and re-cast — the wine is already poured (non-difference); you are the cup. Feeling-tip: warmth as if from a sip; the distance you wanted to close was the fiction.",
 source_path="sources/sivastotravali_corpus.json", source_ref="4.18"),
dict(id="srg-3", section="srgara", title="What Delight, Beloved", source="Kṣemarāja, Ghatakarpara (pot-sherds) v.5",
 iast="ambudaiḥ śikhigaṇo vinādyate kā ratiḥ priya mayā vinādya te",
 en="by clouds the peacock-flock is sounded —\nwhat delight, beloved, without me today?",
 brief="Love-in-separation given to the whole landscape — the peacock's cry.",
 logic="Ghatakarpara, Kṣemarāja's night of the broken pot, frames longing as weather: the peacocks cry at cloud-arrival — and the cry is 'without me.' Vipralambha (longing-in-separation) is outsourced to the scene until the self-pity becomes a rainstorm that belongs to everyone. The ache is seasonal, not personal.",
 howto="When longing for someone or something: say it as the peacock line — the cry is appropriate, beautiful, and will end with the rain. Feel the ache as weather: you are the bird, not the drowning.",
 source_path="sources/L4-ghat-p01-v05.DRAFT.json", source_ref="ghat-p01 v5"),
dict(id="srg-4", section="srgara", title="The Moon That Carries the Nectar", corpus=[3,5],
 source="Utpaladeva, Śivastotrāvalī 3.5",
 en="give me one glance of yours — light, cool, pure,\nlike the moon's crescent, carrying nectar —\no lord, for my desire itself.",
 brief="The cool moon-glance that carries desire instead of burning it.",
 logic="Kāma (desire) is not banned here but delivered amṛta: the verse asks for a dṛś, a gaze that is śītalā (cool) like the moon's crescent and amṛta-vāhinī (nectar-bearing). The erotic voltage of rati is converted into moonlight — desire needs cooling and nourishment, not cutting.",
 howto="When desire runs hot: one breath in, offer the heat upward as the thing that needs the glance, and picture the crescent-cool gaze landing on it. The prayer cools by image, not by prohibition. Feeling-tip: the heat stays but stops being an emergency.",
 source_path="sources/sivastotravali_corpus.json", source_ref="3.5"),
# ---------------- II. HĀSYA ----------------
dict(id="has-1", section="hasa", title="Laughing, Dancing, Eating It All", corpus=[5,18],
 source="Utpaladeva, Śivastotrāvalī 5.18",
 en="where he laughs and dances, where desire and hatred themselves are eaten,\nwhere the nectar-rasa of devotion is drunk —\nmay i attain that state.",
 brief="The state where he laughs, dances, and eats the klesas for lunch.",
 logic="Hāsa's sthāyin hāsa is made cosmic: the divine one laughs and dances, and — the key verb — rāga-dveṣe bhujyate, desire and hatred are CONSUMED as food. Mirth here is not humour; it is the sound of digestion. The negative emotions are not banished from the state; they are the meal.",
 howto="Say it when something finally stops being infuriating — and notice the laugh that arrives is the verse working. Feeling-tip: the annoyance is suddenly chewable; that is bhujyate happening. Let the laugh be the proof.",
 source_path="sources/sivastotravali_corpus.json", source_ref="5.18"),
dict(id="has-2", section="hasa", title="The Essence of Laughter", corpus=[2,18],
 source="Utpaladeva, Śivastotrāvalī 2.18",
 en="in this three-world joke whose essence is laughter —\nto you alone, the non-dual, the one seated in eternal joy:\nnamas.",
 brief="Bowing to the Lord who sits on laughter itself.",
 logic="The universe is upahāsa-ekasāra — the essence of the cosmic joke — and the Lord is nitya-sukha-āsina, seated in eternal joy. Laughter is not irreverence but the metaphysical register of the world-as-play seen from inside. You bow TO the seated laughter rather than laughing at him: reverence and joke in one breath.",
 howto="When life turns absurd: say it, and read the absurdity as his seat. Feeling-tip: irreverence without disrespect — the sigh turns into a chuckle, and the chuckle lands on him.",
 source_path="sources/sivastotravali_corpus.json", source_ref="2.18"),
dict(id="has-3", section="hasa", title="His Laughing-Play", corpus=[3,15],
 source="Utpaladeva, Śivastotrāvalī 3.15",
 en="victorious are your servants, lord of the worlds —\nfor whom this ocean of saṃsāra\nis a laughing-play.",
 brief="Same ocean as everyone else's; for his servants it's a playground.",
 logic="Everyone else drowns in saṃsārārṇava — the ocean of becoming. For yeṣāṃ (for those servants) it is krīḍā-hāsara: a park of laughter and play. Hāsa changes the ownership of the ocean, not its water. The rasa-shift happens before the circumstance shifts — the ocean is the fact, the playground is the flavour.",
 howto="In a hard moment, name it: ocean. Then say the verse, and the water becomes shallow. Feeling-tip: the shoulders drop and the mouth lifts before the situation changes at all.",
 source_path="sources/sivastotravali_corpus.json", source_ref="3.15"),
dict(id="has-4", section="hasa", title="Angry, Then Laughing, Then Śiva", corpus=[16,7],
 source="Utpaladeva, Śivastotrāvalī 16.7",
 en="let me be drunk on devotion — and angry with the world,\nand pitying it — then laugh, and rise up, and shout:\nśiva! — enough.",
 brief="The permission slip: devotion lets you rage, then laugh, then shout.",
 logic="The verse gives the full emotional sequence and blesses every step: bhakti-kṣīva (drunk on devotion) → kupyeyam (let me be angry!) → haseyaṃ (then laugh) → udyām (rise) → raṭeyam śivety (shout Śiva). Anger is not the failure of the practice but its middle passage — it converts to laughter to shout. Hāsa is the hinge where the negative becomes praise.",
 howto="When worked up: say it as an instruction manual — drunk first, then let it become laugh, rise, and shout. The last word must be Śiva, out loud if you dare. Feeling-tip: the anger doesn't get suppressed; it gets promoted.",
 source_path="sources/sivastotravali_corpus.json", source_ref="16.7"),
# ---------------- III. KARUṆĀ ----------------
dict(id="kar-1", section="karuna", title="The Seed of Sorrow", corpus=[1,26],
 source="Utpaladeva, Śivastotrāvalī 1.26",
 en="strange, lord: this mind is by nature the seed of sorrow —\nyet watered with the rasa of your devotion\nit ripens into the highest fruit.",
 brief="The sorrow-seed that ripens instead of rotting.",
 logic="The verse concedes the grief outright: manaḥ is duḥkha-bīja by nature (nisargataḥ) — the mind was born a grief-seed. The surprise (citra!) is the alchemy: watered with bhakti-rasa it becomes niḥśreyasa-mahāphala, the highest fruit. Karuṇā is not healed by removal but by irrigation — the same seed, different harvest.",
 howto="In grief: say it and water the seed instead of cursing the soil. Feeling-tip: the grief stays, but it is being used; even the tears count as irrigation.",
 source_path="sources/sivastotravali_corpus.json", source_ref="1.26"),
dict(id="kar-2", section="karuna", title="The Flood Over Joy and Sorrow", corpus=[3,9],
 source="Utpaladeva, Śivastotrāvalī 3.9",
 en="the flood of nectar from meditating you overflows\njoy and sorrow alike — like waters filling\nall the low and lower lands.",
 brief="One flood levels the hierarchy of gladness and grief.",
 logic="A single amṛta-pūra (flood of nectar from dhyāna) covers harṣa AND śoka samam — equally, like water filling every lowland. Sorrow gets no special treatment and no special exclusion: both emotions are terrain, and the flood is the same. Karuṇā's transformation is levelling, not fixing.",
 howto="Say it in either state — grief or glee — the verse works on the level of the field, not the feeling. Feeling-tip: a settling, as if water found its level; the ranking of emotions collapses.",
 source_path="sources/sivastotravali_corpus.json", source_ref="3.9"),
dict(id="kar-3", section="karuna", title="Sorrow Mixed with Ghee", corpus=[10,16],
 source="Utpaladeva, Śivastotrāvalī 10.16",
 en="lord, the countless sorrows even of the world-dweller —\nmixed with your own self they become ghee:\nthey come to be bearable.",
 brief="Sorrow mixed with Śiva-self becomes ghee — and ghee is bearable.",
 logic="The alchemical verse: duḥkha + bhavat-īya-ātman (your own self) = ghṛta (ghee). Ghee does not remove the ingredient — it transforms its texture: the sharp is suspended in the smooth. The grief survives as substance but not as edge. Karuṇā's medicine is texture change, not argument.",
 howto="In pain: say the ghee line and literally imagine the sharp edge of the feeling being coated. Feeling-tip: the body responds to texture, not to reasons — the tightness loosens because the sharpness is now suspended.",
 source_path="sources/sivastotravali_corpus.json", source_ref="10.16"),
dict(id="kar-4", section="karuna", title="The Banner Against Suffering", corpus=[11,14],
 source="Utpaladeva, Śivastotrāvalī 11.14",
 en="o lord, the banner that destroys the suffering of the bowing —\ntreasure of good, dhūrjaṭa: for me whose only home is sorrow,\nafraid of birth and death — so act for me, that while yet living\ni may enjoy the sweet taste of the good sense-objects,\nunshakeable, the powers in service of your worship.",
 brief="The emergency prayer: grief addressed to the Destroyer-of-pain by name.",
 logic="The Lord is named by function: praṇatārti-nāśana-paṭa — the flag that annihilates the pain of the one who bows. The verse locates the speaker without self-pity: ālaya-eka — sorrow is the only house I know, and I fear birth and death. The grief is fully stated before the name is invoked — confession first, then the banner.",
 howto="At 3am in the pit: say the whole confession first, then the name. Feeling-tip: the banner is real — a flag planted IN the grief, not flying over it. The fear of birth and death can be said out loud; that's the verse's permission.",
 source_path="sources/sivastotravali_corpus.json", source_ref="11.14"),
# ---------------- IV. RAUDRA ----------------
dict(id="rau-1", section="raudra", title="The Axe of 'All Is His'", corpus=[7,2],
 source="Utpaladeva, Śivastotrāvalī 7.2",
 en="'this is mine, this is not yours' — the roots of attachment and aversion, hard-shackled;\no lord, let the axe of the one conviction 'all is your-become' fall on them in me.",
 brief="The engine of rage is mine-ness; the axe is the conviction that all is his.",
 logic="Anger's roots are rāga-dveṣa driven by mamaka (mine-ness) — 'etan mama, na tv idam' (this is mine, this is not yours). The remedy named is an instrument: paraśu, the axe of ekatva-pratyaya — the conviction that everything is bhavanmaya, his-become. The verse PRAYS FOR THE AXE TO FALL — an act, not a mood.",
 howto="In rage: name the possession first — 'mine', 'not yours' — then say the verse at it. Feeling-tip: the fist unclenches not by relaxing but by losing the ownership record; the thing remains, the claiming ends.",
 source_path="sources/sivastotravali_corpus.json", source_ref="7.2"),
dict(id="rau-2", section="raudra", title="Let the Anger Ripen", corpus=[16,15],
 source="Utpaladeva, Śivastotrāvalī 16.15",
 en="the mind purified by the complete ripening of\nhonour and dishonour, rāga and the rest —\nsuch a devotee: how could he have ordinary-world conduct?",
 brief="Pride, slight and rage treated as things that must fully ripen first.",
 logic="Māna, avamāna (honour and dishonour), rāga — these must NIṢPĀKA, ripen completely, like poison cooked out or fruit brought to sweetness. The purified mind is the one where the indignation-mix has finished its fermentation. The verse reframes the anger-process itself: give it heat and time, and the result is clarity instead of explosion.",
 howto="When slighted: say it and let the feeling ripen rather than react — the insult is being cooked, not served. Feeling-tip: the heat continues but stops being an instruction to act.",
 source_path="sources/sivastotravali_corpus.json", source_ref="16.15"),
dict(id="rau-3", section="raudra", title="Devotion Conquers the Darkness", corpus=[16,16],
 source="Utpaladeva, Śivastotrāvalī 16.16",
 en="in whose case even the darkness of attachment and aversion\nhas been conquered by the brilliance of devotion —\nwhat to speak of the learned, among such exalted ones?",
 brief="Rage is a lightless state; devotion is the light that ends it.",
 logic="Rāga-dveṣa are andhakāra — darkness; bhakti-tviṣ, the brilliance of devotion, is the conqueror. The verse gives light-physics to anger: not fight the dark, but shine. And what remains after conquest is not the repressed but mahīyas — the exalted, lit-up ones. The learned don't even rate in comparison.",
 howto="Say it as a light-switch claim: the anger is dark, and you are switching on devotion rather than wrestling the dark. Feeling-tip: warmth precedes relief — that order is the physics.",
 source_path="sources/sivastotravali_corpus.json", source_ref="16.16"),
dict(id="rau-4", section="raudra", title="Your Wrath Purifies", corpus=[10,20],
 source="Utpaladeva, Śivastotrāvalī 10.20",
 en="also worthy of praise, O supreme, are those\nmade pure by the touch of your wrath's fire\neven when you have destroyed them.",
 brief="Even his wrath is a purifier — so the fire itself is praised.",
 logic="Tvat-kopa-pāvaka — the fire of your wrath — is pāvaka, a purifier, by definition. Those touched (even annihilated) by it are pūtā, purified. Raudra's rasa seen from the other side: divine anger is cauterisation, not punishment. The devotee's praise of THAT is the final surrender of the complaint against anger itself.",
 howto="When caught in a rage — yours or someone's's: say it, and re-classify the fire as purifying touch before responding. Feeling-tip: the flinch converts to a bow.",
 source_path="sources/sivastotravali_corpus.json", source_ref="10.20"),
# ---------------- V. VĪRA ----------------
dict(id="vir-1", section="vira", title="Victory — the World Depends on Him", corpus=[2,29],
 source="Utpaladeva, Śivastotrāvalī 2.29",
 en="victory, lord — namas, namas to you:\nthis entire universe depends on you;\nyou are the supreme lord of the worlds, the one —\nin you alone i take refuge.",
 brief="The victory-cry that puts the whole world on his back.",
 logic="Vīra's sthāyin utsāha begins with jaya — twice — then the cosmic dependency: sakalaṃ viśvam idaṃ tavāśritam, everything rests on YOU. The hero's strength is deliberately outsourced: your energy becomes his vehicle rather than your own inventory. Enthusiasm as alignment, not as ego.",
 howto="Morning, before the task: say it once under the breath, fast. Feeling-tip: the chest widens; effort turns from strain into celebration because the weight is his, not yours.",
 source_path="sources/sivastotravali_corpus.json", source_ref="2.29"),
dict(id="vir-2", section="vira", title="May I Become the Grass", corpus=[5,15],
 source="Utpaladeva, Śivastotrāvalī 5.15",
 en="when, eyes closed in the tasting of inner devotion-wonder,\ni worship 'namas to śiva' —\nmay i become even the grass [in that place].",
 brief="So lost in devotion's wonder one would be the grass at the threshold.",
 logic="The extreme of vīra-bhakti: antar-bhakti-catkāra (inner wonder) savoured until the eyes close (āmīlitekṣaṇa), and the self-offer is to become tṛṇa — grass, trodden, at his doorway. Heroism here is the heroism of disappearance INTO devotion; the glory is to be the least impressive thing present.",
 howto="When enthusiasm needs depth rather than noise: say it and offer to be the least impressive thing in the room. Feeling-tip: the wanting-to-be-seen dissolves; the energy continues without the vanity.",
 source_path="sources/sivastotravali_corpus.json", source_ref="5.15"),
dict(id="vir-3", section="vira", title="The Sound That Never Leaves the Mouth", corpus=[4,14],
 source="Utpaladeva, Śivastotrāvalī 4.14",
 en="victorious those on whose mouth's circle\nthe sound of śiva constantly roams —\never-streaming from the immortal reservoir,\nthe supreme nectar dripping sweet.",
 brief="Victory to the constant chanter — japa become involuntary.",
 logic="Niyataṃ śivadhvaniḥ — the Śiva-sound circulating the face without stop (the gloss: twenty-four hours). Vīra's utsāha here is constancy: practice that has become self-running — the ajapa that the Vijñāna Bhairava describes as breath itself. The verse is a toast to the one whose mantra no longer needs permission.",
 howto="Say it when you catch the name rising on its own — mid-shower, mid-walk. The verse applauds the practice applauding itself. Feeling-tip: pride WITH devotion; the discipline patting itself on the back.",
 source_path="sources/sivastotravali_corpus.json", source_ref="4.14"),
dict(id="vir-4", section="vira", title="Praised Because You Worship", corpus=[4,1],
 source="Utpaladeva, Śivastotrāvalī 4.1",
 en="o mind, though you are flickering, yet you are praised —\nbecause you worship:\nyou take refuge in the refuge of the refuges,\nthe teacher of the three worlds, the beloved of ambikā.",
 brief="The distracted mind is praised for showing up anyway.",
 logic="Capala (flickering, unstable) is normally the enemy of every practice — the verse reverses the verdict: slāghyase, you are PRAISED, yato bhajase, because you worship. Utsāha for the distracted: the measure is not steadiness but direction. Even a scattering mind in the direction of refuge earns the praise.",
 howto="Address it TO your mind, in the second person, when it won't hold — praise it for showing up rather than scolding it for drifting. Feeling-tip: self-compassion as fuel; the scattered mind sits down when praised, not when punished.",
 source_path="sources/sivastotravali_corpus.json", source_ref="4.1"),
# ---------------- VI. BHAYĀNAKA ----------------
dict(id="bha-1", section="bhayanaka", title="When Will I Suddenly Recognise You", corpus=[9,6],
 source="Utpaladeva, Śivastotrāvalī 9.6",
 en="the lord — fearless, generous, full, causeless,\nbeyond denial of self — when will i suddenly recognise him —\nand put the master's own folk to shame?",
 brief="Addressed to the Lord whose very name is fearlessness.",
 logic="Bhayānaka's sthāyin bhaya meets Īśvara who is abhaya — fearless — and the cure named is sahasābhijñā, sudden recognition, not calm. The verse's logic: fear is the pre-recognition static, and kadā — when — is a countdown to the flash. Recognising him puts the world (which produced the fear) to shame.",
 howto="When fear is up: say it as a question, not a plea — kadā? when? Feeling-tip: fear becomes the sound before the recognition rather than the enemy of it. After the last word, expect nothing; the asking is the turning.",
 source_path="sources/sivastotravali_corpus.json", source_ref="9.6"),
dict(id="bha-2", section="bhayanaka", title="The Full Confession", corpus=[11,8],
 source="Utpaladeva, Śivastotrāvalī 11.8",
 en="i am dull, i am weighed with sorrow, i am afraid of old age's flaws,\ni am without power — i have taken refuge in you, o śambhu;\nso calculate what's left.",
 brief="The full inventory — including the fear of decay — ending in refuge.",
 logic="The verse itemises the negative self-image without flinching: mūḍha (dull), duḥkhakṛta (sorrow-woven), jarā-doṣa-bhīta (afraid of old age's flaws), śakti-hīna (powerless) — and then the pivot: tavāśritaḥ asmi, I have taken refuge. Named fears lose volume; the inventory ends in a single act of leaning.",
 howto="List YOUR four in his cadence, then land the last line. Feeling-tip: the inventory leaves the body lighter; the refuge-line is the exhale. Especially for aging-anxiety and inadequacy-shame.",
 source_path="sources/sivastotravali_corpus.json", source_ref="11.8"),
dict(id="bha-3", section="bhayanaka", title="Between His Feet", corpus=[12,8],
 source="Utpaladeva, Śivastotrāvalī 12.8",
 en="residing even between your feet and your devotees' —\ni am without fear; in those various planes of being\ni would worship the lord, unobstructed in action.",
 brief="Fearlessness by geography: living in the gap between his feet.",
 logic="Nivasann antara eva nirbhayaḥ — dwelling in the in-between (between his feet and his people), fearlessness arises not from courage but from LOCATION. The verse gives fear a map: there is a narrow country, foot-adjacent and community-adjacent, where bhaya simply has no border. Fear lives at other addresses.",
 howto="When fear arrives: find the location instead of fighting the feeling. Imagine the small warm space between his feet; move in. Feeling-tip: the fear stays outside the border like weather reported from another city.",
 source_path="sources/sivastotravali_corpus.json", source_ref="12.8"),
dict(id="bha-4", section="bhayanaka", title="The Scorching Dissolved", corpus=[9,18],
 source="Utpaladeva, Śivastotrāvalī 9.18",
 en="when will i come to dwell in the drinking-and-playing\nof your devotion-nectar — with the eight powers attained,\nand all fear of troubles dissolved?",
 brief="Anticipatory dread melts in the rasa-cup.",
 logic="Two claims: the eight siddhis may be attained (the vīra-bait), but the real payload is vigalita-upātāpa-santrāsa — the dread-of-burn having MELTED in the rāsa-drinking. Upātāpa is the scorching anxiety of what's coming; it isn't fought, it is dissolved in the cup. Fear as something you drink through.",
 howto="Anxious about what's coming? Take the verse as a drink-description and sip your current state as rasa. Feeling-tip: the anticipatory heat cools; the future stops glowing red.",
 source_path="sources/sivastotravali_corpus.json", source_ref="9.18"),
# ---------------- VII. BĪBHATSA ----------------
dict(id="bib-1", section="bibhatsa", title="The Smear That Is Forgetting", corpus=[13,2],
 source="Utpaladeva, Śivastotrāvalī 13.2",
 en="even within, the tiniest smear that is my non-contemplation of you —\nwiping that, o lord, from everywhere,\n[show] your own form.",
 brief="The impurity isn't filth; it's the lapse of remembering.",
 logic="The mala is tvad-apratana-kālikā — even the moment's failure to think of him. Bībhatsa's disgust, redirected: the thing that disgusts is not dirt but forgetting. And the wiping (parimṛjya) reveals svarūpa — the cleaner the frame, the more the face shows. Disgust at the stain becomes longing for what the stain hid.",
 howto="In self-loathing: rename the stain — it is just the lapse of attention. Wipe = return, not scrub. Feeling-tip: the self-hatred loses its subject, and what's left is a fresh look at his form.",
 source_path="sources/sivastotravali_corpus.json", source_ref="13.2"),
dict(id="bib-2", section="bibhatsa", title="The Impure Mind, Confessed", corpus=[15,14],
 source="Utpaladeva, Śivastotrāvalī 15.14",
 en="in my mind, absolutely impure, my own devotion-vine drowned —\nhard: it ripens not even its own,\nthe unearned blossoms of its fortune.",
 brief="The raw confession — the devotion-vine drowned in muck.",
 logic="Bībhatsa at its least polite: maline manasi, the mind is dirty, and the bhakti-latā (devotion-vine) is submerged under it — so even its own virtues don't ripen. Utpaladeva includes the complaint in the hymn-book itself: self-disgust, spoken, IS bhakti's material. The shame is not edited out; it is a verse.",
 howto="Say it on the days you feel worst about yourself — the hymn says it for you, better. Feeling-tip: honesty displaces shame; the muck, spoken aloud, is at least seen.",
 source_path="sources/sivastotravali_corpus.json", source_ref="15.14"),
dict(id="bib-3", section="bibhatsa", title="The Doubt-Enemy Shattered", corpus=[18,19],
 source="Utpaladeva, Śivastotrāvalī 18.19",
 en="the thought-stain in my mind, scoured by the deathless nectar's flood\npoured over the trough of refuse — with the invincible doubt-enemy crushed:\nlet beholding you be unceasing.",
 brief="The stain's partner in crime is doubt — and seeing breaks both.",
 logic="The verse names the double-bind: mala (the mind's stain) and the durjaya saṃśaya-vairin (the invincible doubt-enemy). Both are destroyed by ONE thing: tvad-avalokana-janita-phala — the fruit born of beholding him. Disgust's cure is not more scrubbing but darśana, the look. The enemy of clarity was never dirt; it was the un-looked-at.",
 howto="When the mind feels stained AND doubting: stop scrubbing, start looking — one look inward at the form. Feeling-tip: doubt and disgust fall together because they were both standing in the dark.",
 source_path="sources/sivastotravali_corpus.json", source_ref="18.19"),
dict(id="bib-4", section="bibhatsa", title="Strike the Dividing-Piece", source="Abhinavagupta, Kramastotra 19.19",
 iast="vilīne śaṅkaughe sapadi paripūrṇe ca vibhave | saṃhārākhyā mama hṛdi bhidāṃśaṃ praharatu",
 en="in the melted doubt-heap, at once in full glory —\no lord named dissolution, strike the split portion of my heart.",
 brief="The hunger that keeps cutting — finished when doubt melts.",
 logic="Kramastotra's verse from Abhinavagupta's own recitation-list: śaṅkaugha (the doubt-flood) is gone, pūrṇa (fullness) stands — and then ONE request: strike the hṛdi-bhidāṃśa, the fragment that divides the heart. The disgust behind bībhatsa was the partition-making: the inner cutter that keeps fullness in two halves. Saṃhāra (dissolution) finishes the surgery.",
 howto="After weeks of inner division — this vs that, me vs it: say it as the surgeon's request, once. Feeling-tip: the split seals; the hunger to divide ends with the knife that isn't yours.",
 source_path="sources/L4-kram-p19.DRAFT.json", source_ref="kram-p19 v19"),
# ---------------- VIII. ADBHUTA ----------------
dict(id="adb-1", section="adbhuta", title="The Wonder of the Word at Tongue-Tip", corpus=[1,20],
 source="Utpaladeva, Śivastotrāvalī 1.20",
 en="when the single word śiva stands ever at the tongue's tip —\nthe taste of all sense-objects exists in the devotee alone.\nwhat a wonder!",
 brief="One word at tongue-tip transmutes every taste into rasa.",
 logic="The verse compresses Vijñāna: the mantra at the organ of taste (jihvāgra) transmutes all viṣaya-āsvāda — every sense-object is tasted as devotion. The aho! is technical: it is vismaya at the mechanism itself — wonder as the experience of the doctrine working. Adbhuta is testable in one bite.",
 howto="When anything tastes or sounds flat: place Śiva at the tongue's tip and re-taste the next sip or bite. Feeling-tip: the wonder is measurable — if the flavour deepens, the verse is real.",
 source_path="sources/sivastotravali_corpus.json", source_ref="1.20"),
dict(id="adb-2", section="adbhuta", title="The Wonderful Deceiver", corpus=[2,12],
 source="Utpaladeva, Śivastotrāvalī 2.12",
 en="namas to the deceptive, the pure, the secret,\nthe manifest-self, the subtle, the all-form —\nto the citra, to śambhu.",
 brief="Bowing to the wonderful one whose wonder IS his trick.",
 logic="Citra — variegated, marvellous, strange — is the epithet running through the verse, married to māyāvine (the deceiver), prakaṭātmane (the manifest secret). The universe's strangeness is his craft, not a malfunction. Adbhuta here is delight in the trick: the weirdness of the world is filed as artistry.",
 howto="When the world turns surreal — say the verse and file the strangeness under citra. Feeling-tip: the uncanny flips from threat to artistry; the trick becomes someone's excellent work.",
 source_path="sources/sivastotravali_corpus.json", source_ref="2.12"),
dict(id="adb-3", section="adbhuta", title="The Wheel of Diverse States", source="Abhinavagupta, Gītārthasaṅgraha v.1",
 iast="ya eṣa vitatasphuradvividhabhāvacakrātmakaḥ parasparavibhedavānviṣayatāmupāgacchati yadekamayabhāvanāvaśata etyabhedānvayaṃ sa śaṃbhuraśivāpaho jayati bodhabhāsāṃ nidhiḥ",
 en="he who, made of the widely flashing wheel of diverse states, comes to be the objects of experience — whose one, given to contemplation, is the bond of non-difference: he, śaṃbhu, averter of woe, triumphs — treasury of the lights of knowing.",
 brief="Abhinavagupta's own opening: the wheel of states resolves into one — triumph.",
 logic="The Gītārthasaṃgraha's first breath performs its thesis: the flash-wheel of manifold states (thoughts, emotions, the day's weather — the very stuff of experience) resolves into abheda, non-difference — and that resolution is jayati, triumph. Adbhuta as the wonder OF the doctrine: the many flashing states are not noise but the treasury-house (nidhi) of knowing-light.",
 howto="Use it as the invocation before any prayer-session in this book: name the swirl of your current states as the wheel, then remember the wheel IS the treasury. Feeling-tip: the chaos of feelings gets reclassified as treasure on sight.",
 source_path="sources/L4-gita-a00-v01.DRAFT.json", source_ref="gita-a00 v1"),
dict(id="adb-4", section="adbhuta", title="Worship Without Begging", corpus=[17,24],
 source="Utpaladeva, Śivastotrāvalī 17.24",
 en="wonder! o boon-giver: among the full-hearted in devotion toward you,\nis any mode of worship praised\nthat is not stained with begging?",
 brief="The great wonder: worship with no shopping list attached.",
 logic="Vismaya at the bhaktas whose pūjā carries no yācñā — no begging-stain. The worship without a price-tag is the marvel; the wonder is the devotee's purity of motive, not the display. Adbhuta turns inward: amazed at the possibility of asking for nothing.",
 howto="Notice when you've prayed with a shopping list. Say this verse as the correction, then worship once with nothing attached. Feeling-tip: the ask drops and the song stays — that gap is the wonder.",
 source_path="sources/sivastotravali_corpus.json", source_ref="17.24"),
# ---------------- IX. ŚĀNTA ----------------
dict(id="san-1", section="santa", title="The Rasa Beyond the World", corpus=[1,21],
 source="Utpaladeva, Śivastotrāvalī 1.21",
 en="diving in the ocean of devotion's nectar — with peaceful waves,\ncool and white and sweet — tasting the alaukika rasa:\nwho among the steady even counts a name there?",
 brief="Śānta's theory in one verse: the peaceful ocean, the non-worldly taste.",
 logic="Everything the Abhinavabhāratī says about rasa is here: śānta-kallola — the peace-wave ocean; svādubhakti-sudhāmbudhi — the nectar-ocean of sweet devotion; and alaukika-rasa-āsvāda — the BEYOND-WORLDLY tasting. Peace is not absence but the most extreme flavour, so intense that the steady (susthā) stop counting even names.",
 howto="For peace-practice: dive once, taste once, count nothing — not even the breath. Feeling-tip: the mental to-do list stops being readable; that illegibility is the alaukika flicker.",
 source_path="sources/sivastotravali_corpus.json", source_ref="1.21"),
dict(id="san-2", section="santa", title="All Time in the Worship-Union", corpus=[17,12],
 source="Utpaladeva, Śivastotrāvalī 17.12",
 en="may all my time — even the endless kind — pass\nin the happiness of union with your worship;\nthat alone is what i crave.",
 brief="The peaceful life defined: every hour inside the worship-union.",
 logic="Kāla (time) is the anxious substance — endless time is the dread of the future. The verse re-routes every hour into bhavat-pūjāmaya-saṅga-sukha, the happiness of joining-with-worship. Śānta as temporal peace: not a mood but a schedule filled with one activity. And the craving (īyadarthaye) is permitted — it is the only thirst worth keeping.",
 howto="When the day stretches ahead daunting: pray the WHOLE day into the worship-frame, then do the next ordinary thing as its first item. Feeling-tip: the horizon softens; time becomes a room, not a corridor.",
 source_path="sources/sivastotravali_corpus.json", source_ref="17.12"),
dict(id="san-3", section="santa", title="For Peace, Not for Pleasure", corpus=[18,15],
 source="Utpaladeva, Śivastotrāvalī 18.15",
 en="for peace, not for pleasure-seeking — those intoxicated\nwith the fullness of your devotion, o lord;\neven the fruit of searching for liberation they don't crave —\nbefore you, the heart-stealer.",
 brief="The anti-materialist verse: peace sought as peace, not as payoff.",
 logic="The devotee's intoxication aims at śāntaye — peace — na sukhalipsutā, explicitly NOT the pleasure-hunt; even mokṣa-phala (the fruit of liberation) is not craved. Śānta is the only desire that cancels desiring — and the verse says so without smugness: these ones don't even want the prize.",
 howto="When peace turns into another acquisition-plan — this retreat, that technique, the next course — say it as the disarming. Feeling-tip: the goal releases you; the practice continues unburdened.",
 source_path="sources/sivastotravali_corpus.json", source_ref="18.15"),
dict(id="san-4", section="santa", title="Cries Like Bamboo-Drops", corpus=[11,9],
 source="Utpaladeva, Śivastotrāvalī 11.9",
 en="laying my cries at your ear's place, my dearest —\nthey grow small: like rain inside a bamboo-joint,\nthey rise as pearls.",
 brief="Even the cries get smaller when laid at his ear.",
 logic="The simile IS the practice: ākranda (cries) laid at his ear-shore become tucchatarāṇi — tinier — like rain slipping down inside a hollow bamboo. Śānta as acoustics: devotion is the volume knob. No silencing, no denial — just the difference between shouting into the void and speaking into an ear.",
 howto="When crying or complaining: say it and consciously LAY the noise at his ear — the listener inside. Feeling-tip: the sound gets smaller mid-sentence; the bamboo-joint is the quiet place behind your own listening.",
 source_path="sources/sivastotravali_corpus.json", source_ref="11.9"),
]


def deva(iast):
    if _tr is None:
        return ""
    try:
        out = _tr(iast, sanscript.IAST, sanscript.DEVANAGARI)
    except Exception:
        return ""
    return out.replace("\U0000A8F3", "\u0902").replace("\U0000A8F2", "\u0901")


def load():
    corpus = json.load(open(HERE / "sources" / "shivastotravali_corpus.json"))
    idx = {(c["number"], v["number"]): v for c in corpus["chapters"] for v in c["verses"]}
    out = []
    for e in E:
        e = dict(e)
        if "corpus" in e:
            v = idx[tuple(e["corpus"])]
            e["iast"], e["devanagari"] = v["iast"], v["devanagari"]
        else:
            e["devanagari"] = deva(e["iast"])
        out.append(e)
    return out


def esc(s):
    return html.escape(s or "")


def dev_size(e):
    L = len(e["devanagari"])
    if L <= 90: return "40pt", "2.0"
    if L <= 150: return "32pt", "1.9"
    if L <= 240: return "25pt", "1.8"
    if L <= 340: return "20pt", "1.75"
    return "16pt", "1.7"


def en_size(e):
    L = sum(len(x) for x in e["en"].split("\n"))
    if L <= 140: return "15pt"
    if L <= 240: return "13.5pt"
    return "12.5pt"


def build_html(entries):
    css = """
@font-face{font-family:'Tiro';src:url('fonts/TiroDevanagariSanskrit-Regular.ttf');}
@font-face{font-family:'Cormorant';src:url('fonts/CormorantGaramond[wght].ttf');font-weight:400 700;}
:root{--ink:#17140f;--grey:#76736e;--hair:#d9d5cc;}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#efece5;color:var(--ink);}
body{font-family:'Cormorant',Georgia,serif;font-size:15pt;line-height:1.5;}
.page{background:#fff;width:148mm;min-height:210mm;margin:0 auto 10mm;padding:20mm 18mm;
  box-shadow:0 2px 14px rgba(0,0,0,.12);position:relative;page-break-after:always;}
.spread{display:flex;gap:8mm;justify-content:center;flex-wrap:wrap;margin:0 auto 10mm;}
.spread .page{margin:0;}
.cover{display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;}
.cover .om{font-family:'Tiro';font-size:60pt;line-height:1;margin-bottom:14mm;}
.cover h1{font-family:'Cormorant';font-weight:600;font-size:36pt;letter-spacing:.05em;margin:0;text-transform:uppercase;}
.cover .sub{font-size:16pt;font-style:italic;color:var(--grey);margin-top:4mm;}
.cover .rule{width:40mm;height:1px;background:var(--ink);margin:10mm auto;}
.cover .blurb{font-size:11pt;text-transform:uppercase;letter-spacing:.14em;color:var(--grey);}
.epi{display:flex;flex-direction:column;justify-content:center;}
.epi.center{align-items:center;text-align:center;}
.epi .lines{font-size:14pt;line-height:1.7;}
.epi .src{font-size:9.5pt;letter-spacing:.15em;text-transform:uppercase;color:var(--grey);margin-top:8mm;}
h2.blk{font-family:'Cormorant';font-weight:600;font-size:15pt;letter-spacing:.08em;text-transform:uppercase;margin:6mm 0 3mm;color:var(--ink);}
.epi p{font-size:13pt;line-height:1.55;margin:0 0 3.5mm;color:#241f19;}
.epi table{border-collapse:collapse;font-size:12pt;width:100%;}
.epi th{text-align:left;font-size:9.5pt;letter-spacing:.14em;text-transform:uppercase;color:var(--grey);border-bottom:1px solid var(--ink);padding:2mm 2mm 2mm 0;font-weight:400;}
.epi td{padding:1.8mm 2mm 1.8mm 0;border-bottom:1px solid var(--hair);}
.epi td.s{font-style:italic;color:var(--grey);}
.toc h2,.sec-div h2,.bib h2{font-family:'Cormorant';font-weight:600;letter-spacing:.12em;text-transform:uppercase;font-size:13pt;color:var(--grey);}
.toc ol{list-style:none;padding:0;margin:5mm 0 0;}
.toc .sec{margin-top:3.5mm;font-size:9.5pt;letter-spacing:.18em;text-transform:uppercase;color:var(--grey);line-height:1.2;}
.toc li{margin:.4mm 0;font-size:11.5pt;line-height:1.3;}
.toc .n{color:var(--grey);display:inline-block;width:7mm;}
.sec-div{display:flex;flex-direction:column;justify-content:center;text-align:center;}
.sec-div .num{font-family:'Cormorant';font-size:11pt;letter-spacing:.3em;color:var(--grey);}
.sec-div h2{font-size:26pt;letter-spacing:.06em;margin:4mm 0 0;color:var(--ink);text-transform:none;font-weight:600;}
.sec-div .sub{font-style:italic;color:var(--grey);font-size:13pt;margin-top:3mm;}
.sec-div .gloss{font-size:10pt;color:var(--grey);margin-top:2.5mm;letter-spacing:.01em;}
.sec-div .rule{width:30mm;height:1px;background:var(--ink);margin:7mm auto 0;}
.sec-div .doc{font-size:11pt;line-height:1.5;color:#241f19;max-width:108mm;margin:7mm auto 0;font-style:italic;}
.src{font-size:9.5pt;letter-spacing:.12em;text-transform:uppercase;color:var(--grey);}
.prayer h3,.guide h3{font-family:'Cormorant';font-weight:600;font-size:17pt;margin:2mm 0 4mm;text-align:center;}
.prayer .dev{font-family:'Tiro';text-align:center;white-space:pre-line;margin:6mm 0 0;}
.prayer .iast{font-style:italic;color:var(--grey);text-align:center;font-size:11pt;line-height:1.5;margin-top:3mm;}
.prayer .en{margin:8mm 0 0;text-align:center;line-height:1.65;color:#241f19;}
.prayer .en .ln{display:block;}
.guide .label{font-size:9pt;letter-spacing:.24em;text-transform:uppercase;color:var(--grey);margin-bottom:3mm;}
.guide h3{text-align:left;font-size:19pt;margin:0 0 3mm;}
.guide .src{text-align:left;margin-bottom:4mm;}
.guide .brief{font-style:italic;color:var(--grey);font-size:11.5pt;line-height:1.45;padding-bottom:3mm;margin-bottom:4mm;border-bottom:1px solid var(--hair);}
.guide .blk{margin-bottom:4mm;}
.guide .bl{font-size:8.5pt;letter-spacing:.2em;text-transform:uppercase;color:var(--grey);display:block;margin-bottom:1mm;}
.guide .body{font-size:11.5pt;line-height:1.55;color:#241f19;}
.guide .body p{margin:0;}
.guide .foot{margin-top:auto;border-top:1px solid var(--hair);padding-top:3mm;font-size:9pt;color:var(--grey);}
.guide .foot a{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--hair);}
.pnum{position:absolute;bottom:10mm;left:0;right:0;text-align:center;font-size:9pt;color:var(--grey);letter-spacing:.1em;}
@media print{html,body{background:#fff}.page{margin:0;box-shadow:none;width:auto;min-height:auto}.spread{display:block;margin:0}@page{size:A5;margin:0}}
"""
    pages = []
    pages.append(f"""<section class="page cover">
<div class="om">ॐ</div>
<h1>{esc(META['title'])}</h1>
<div class="sub">{esc(META['subtitle'])}</div>
<div class="rule"></div>
<div class="blurb">{esc(META['blurb'])}</div>
</section>""")

    pages.append(f"""<section class="page epi center"><div class="lines">{esc(deva(META['epi_iast']))}</div>
<div class="src">{esc(META['epi_src'])}</div></section>""")

    # --- INTRO1: what is a rasa ---
    pages.append("""<section class="page epi">
<h2 class="blk">What is a rasa?</h2>
<p>Every feeling you will ever have — fear, grief, rage, delight — is already a particular
<b>camatkāra</b> of consciousness. Wonder is not one emotion among others; it is the primary
characteristic of consciousness itself (Tantrāloka, ad 1/53), and perception itself is an act
of wonder (TĀ 1260–68). “The mental fluctuations of anger and the like exist because they
are one with the wonder that is the experience of consciousness” (TĀ 15254).</p>
<p>So the door is not something to build. Anxiety is consciousness in one of its flavours;
grief is another. Abhinavagupta's most radical claim follows: <b>all rasas are essentially
pleasurable — even the painful emotions</b>, and “the nature of suffering is, essentially, a
particular kind of wonder” (TĀ 25585–94). Emotions only “lend variety to the enjoyment of
this bliss.”</p>
<p>This book does not argue you out of any feeling. It re-tastes them: the move from
<b>felt-AT</b> to <b>savoured-AS</b> — what Sanskrit poetics calls objectification and
sādhāraṇīkaraṇa — and the savour is recognition wearing that emotion's face.</p>
<div class="src">Theory: Abhinavabhāratī &amp; Tantrāloka, via the house rasa sessions</div></section>""")

    # --- INTRO2: the nine ---
    rows = ""
    for k, (t, conv, door) in {
      "srgara": ("Śṛṅgāra", "the Erotic", "love, longing"),
      "hasa": ("Hāsya", "the Comic", "mirth, laughter"),
      "karuna": ("Karuṇā", "the Pathetic", "grief, compassion"),
      "raudra": ("Raudra", "the Furious", "fury, rage"),
      "vira": ("Vīra", "the Heroic", "valour, energy"),
      "bhayanaka": ("Bhayānaka", "the Horrible", "fear, terror"),
      "bibhatsa": ("Bībhatsa", "the Disgusting", "disgust, loathing"),
      "adbhuta": ("Adbhuta", "the Marvellous", "wonder, awe"),
      "santa": ("Śānta", "the Peaceful", "peace (his ninth)")}.items():
        lit = GLOSS[k].split("— ",1)[1].split(" (")[0].strip('"')
        sth = DOCTRINE[k].split("sthāyin: ",1)[1].split(" —")[0]
        rows += f"<tr><td>{t}<br><span style='font-size:9.5pt;color:#76736e'>{lit}</span></td><td><b>{conv}</b></td><td class='s'>{door}</td><td class='s'>{sth}</td></tr>"
    pages.append(f"""<section class="page epi">
<h2 class="blk">The nine rasas</h2>
<p>The classical table of nine (Nāṭyaśāstra), fixed by Abhinavagupta in his
Abhinavabhāratī — where he added the ninth, śānta. Each rasa carries its <b>sthāyibhāva</b>,
the permanent emotion beneath it. Four prayers per rasa; each section's divider gives the
literal sense, the conventional term, the sthāyin and the doctrine.</p>
<table><tr><th>Rasa &amp; its literal sense</th><th>Conventional</th><th>The door</th><th>Sthāyin</th></tr>{rows}</table>
<div class="src">Nāṭyaśāstra · Abhinavabhāratī · Monier-Williams glosses · thirty-six prayers inside</div></section>""")

    # --- INTRO3: how to use ---
    pages.append("""<section class="page epi">
<h2 class="blk">How to use a doorway</h2>
<p><b>1 — Name it.</b> Say what the feeling actually is, plainly: fear, jealousy, boredom.
Objectifying is the first half of sādhāraṇīkaraṇa — the feeling stops being you.</p>
<p><b>2 — Stay one breath.</b> Do not fix, do not flee. The rasa is alaukika — beyond time
and space — yet felt (sva-saṁvedana). Staying lets it be what it is: consciousness
tasting itself in that key.</p>
<p><b>3 — Recognise.</b> Ask: whose camatkāra is this? The answer is already the
book's thesis — it is the one taste wearing the emotion. That flicker is recognition.</p>
<p><b>4 — Say the prayer.</b> The verse is the re-tasting instrument. It does not
banish the feeling; it converts felt-AT into savoured-AS. Read the guide once when you
meet a prayer; after that, the prayer page alone is enough.</p>
<p style="color:#76736e;font-size:11pt">Sources: verses from our Kashmir Shaiva corpus
(translation-work) — Abhinavagupta, Utpaladeva, Kṣemarāja, Vasugupta — each linked from its
guide. Theory quotes are short and attributed; verify against print editions before study.</p>
<div class="src">Tantric Prayer</div></section>""")

    toc = ['<section class="page toc"><h2>Contents</h2><ol>']
    n = 0
    for sid, num, title, sub in SECTIONS:
        toc.append(f'<div class="sec">{num} &nbsp; {esc(title)} <span style="opacity:.6">{esc(sub)}</span></div>')
        for e in [x for x in entries if x["section"] == sid]:
            n += 1
            toc.append(f'<li><span class="n">{n}</span>{esc(e["title"])}</li>')
    toc.append("</ol></section>")
    pages.append("".join(toc))

    n = 0
    for sid, num, title, sub in SECTIONS:
        pages.append(f"""<section class="page sec-div"><div class="num">{esc(num)}</div>
<h2>{esc(title)}</h2><div class="sub">{esc(sub)}</div>
<div class="gloss">{esc(GLOSS[sid])}</div><div class="rule"></div>
<div class="doc">{esc(DOCTRINE[sid])}</div></section>""")
        for e in [x for x in entries if x["section"] == sid]:
            n += 1
            ds, dlh = dev_size(e)
            es = en_size(e)
            en_lines = "".join(f'<span class="ln">{esc(l)}</span>' for l in e["en"].split("\n"))
            pages.append(f"""<div class="spread">
<section class="page prayer">
<div class="src">{esc(e['source'])}</div>
<h3>{esc(e['title'])}</h3>
<div class="dev" style="font-size:{ds};line-height:{dlh}">{esc(e['devanagari'])}</div>
<div class="iast">{esc(e['iast'])}</div>
<div class="en" style="font-size:{es}">{en_lines}</div>
<div class="pnum">{n}</div></section>
<section class="page guide">
<div class="label">The Guide</div>
<h3>{esc(e['title'])}</h3>
<div class="src">{esc(e['source'])} · {esc(e['source_ref'])}</div>
<div class="brief">{esc(e['brief'])}</div>
<div class="body">
<div class="blk"><span class="bl">What is happening</span><p>{esc(e['logic'])}</p></div>
<div class="blk"><span class="bl">How to use it</span><p>{esc(e['howto'])}</p></div>
</div>
<div class="foot">Source: <a href="{esc(e['source_path'])}">{esc(e['source_path'].replace('sources/',''))} · {esc(e['source_ref'])}</a></div>
<div class="pnum">{n} · guide</div></section>
</div>""")

    pages.append(f"""<section class="page epi center"><div class="lines" style="font-family:'Tiro'">ॐ शान्तिः शान्तिः शान्तिः</div>
<div class="src">Tantric Prayer</div></section>""")

    seen, blist = set(), []
    for e in entries:
        p = e.get("source_path")
        if p and p not in seen:
            seen.add(p)
            refs = [x["source_ref"] for x in entries if x.get("source_path") == p]
            blist.append((p, refs))
    bib = ['<section class="page bib"><h2>Sources</h2><ul>']
    for p, refs in blist:
        bib.append(f'<li><b>{esc(p.replace("sources/","").replace("-"," "))}</b><br>'
                   f'<a href="{esc(p)}">{esc(p)}</a><br>'
                   f'<span style="color:#76736e;font-size:9.5pt">{esc(", ".join(refs))}</span></li>')
    bib.append('<li><b>Śivastotrāvalī corpus (33 verses)</b><br>'
               '<a href="sources/shivastotravali_corpus.json">sources/shivastotravali_corpus.json</a></li>')
    bib.append('</ul></section>')
    pages.append("".join(bib))

    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(META['title'])} — {esc(META['subtitle'])}</title>
<style>{css}</style></head><body>{''.join(pages)}</body></html>"""
    (HERE / "index.html").write_text(doc, encoding="utf-8")


def build_json(entries):
    (HERE / "prayers.json").write_text(
        json.dumps({"meta": META, "entries": entries, "count": len(entries)},
                   ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    entries = load()
    build_json(entries)
    build_html(entries)
    print(f"prayers: {len(entries)}")
    for sid, num, title, sub in SECTIONS:
        print(f"  {num}. {title:<12} {len([x for x in entries if x['section']==sid])}")
    bad = [e["id"] for e in entries if not e.get("devanagari") or not e.get("iast") or not e.get("guide") and not e.get("logic")]
    print("incomplete:", [e for e in bad] or "none")
