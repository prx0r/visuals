#!/usr/bin/env python3
"""Practical Prayers — forty Trika prayers for the moments of the day
Prayer page (type-filling Devanagari, Brahmārpaṇaṁ format) + facing explanation.
Run with the patala venv python (indic_transliteration)."""

import json, html, pathlib, re
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from stencils import activity_glyph

HERE = pathlib.Path(__file__).parent
try:
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate as _tr
except Exception:
    _tr = None

META = dict(
    title="Practical Prayers",
    subtitle="Forty prayers for the moments of the day — with Swamiji's sangha hymns",
    blurb="waking · bathing · social · work · food · waiting · negative · positive · evening",
    epi_iast="brahmārpaṇaṁ brahma havir brahmāgnau brahmaṇā hutam",
    epi_en="the offering is brahman, the oblation is brahman, poured by brahman into the fire of brahman",
    epi_src="Bhagavad Gītā 4.24 — the meal prayer",
)

SECTIONS = [
    ("wake", "I", "Waking / Morning", "on rising"),
    ("bath", "II", "Bathing", "water & body"),
    ("social", "III", "Social", "out among people"),
    ("work", "IV", "At Work", "at the desk"),
    ("food", "V", "Food", "before eating"),
    ("wait", "VI", "Waiting", "in the in-between"),
    ("negative", "VII", "When You Are Negative", "fear · doubt · grief"),
    ("sick", "VIII", "When You Are Sick", "illness · pain"),
    ("positive", "IX", "When You Are Positive", "rejoice · devote"),
    ("sleep", "X", "Evening / Sleep", "wind down · lights out"),
    ("sangha", "A", "Chanted at the Sangha", "Swamiji's hymns of protection"),
]

# corpus refs: (chapter, verse) into shivastotravali_corpus.json
E = [
dict(id="gita-424", section="food", title="The Meal Offering",
 source="Bhagavad Gītā 4.24 (Lakshmanjoo mealtime yajña)",
 iast="brahmārpaṇaṁ brahma havir brahmāgnau brahmaṇā hutam | brahmaiva tena gantavyaṁ brahmakarmasamādhinā ||",
 en="the offering is brahman / the oblation is brahman / poured by brahman into the fire of brahman / brahman alone is reached / by one absorbed in the action that is brahman",
 brief="The meal prayer: water in the palm, one verse, and eating becomes worship.",
 logic="Lakshmanjoo read brahman throughout as Lord Śiva. Four things are named — the offering, the oblation, the fire, the goal — and all four are the same substance. What you take is offered to Śiva; what you offer is itself Śiva; the stomach is Śiva's residence. The logic collapses the distance between eater, food and eaten into one taste.",
 howto="Before the first bite: put a little water in the palm, look at the food, and say the verse once. Then eat as if the meal is being offered into a fire — slowly, without hurry. The feeling to find: gratitude with heat. Nothing extra; the verse does the whole work.",
 source_path="sources/mealtime-yajna.md", source_ref="Gītā 4.24"),
dict(id="somananda", section="food", title="Śiva Bows to Śiva",
 source="Somananda, Śivadṛṣṭi 7.103 (mealtime lore)",
 iast="asmadrūpa samāviṣṭaḥ svātmanātma nivāraṇe | śivaḥ karotu nijayā namaḥ śaktyā tatātmane ||",
 en="śiva, having entered the form that is myself, bows — by his own power — to śiva, for the removal of the obstacle that is himself.",
 brief="The obstacle on the plate is also Śiva. Say it before food.",
 logic="The whole Trika in one bow: the one who bows, the one bowed to, the obstacle being removed, and the power doing the removing are all Śiva. Nothing is outside the recognition — not even the thing that blocks it. Lakshmanjoo taught this verse alongside the mealtime practice.",
 howto="Say it silently as the food arrives. The 'obstacle' can be anything — the craving, the guilt, the person you're eating with. Name it, then let the verse dissolve it. Feeling-tip: the moment of placing should feel like relief, like putting something down.",
 source_path="sources/mealtime-yajna.md", source_ref="Śivadṛṣṭi 7.103 (provisional)"),
dict(id="deha-5", section="food", title="The Sense-Goddesses Offer Bhairava",
 source="Dehastha v.5",
 iast="ātmīyaviṣayabhogairindriyadevyaḥ sadā hṛdambhoje | abhipūjayanti yaṃ taṃ cinmayamānandabhairavaṃ vande",
 en="with feasts of their own sense-objects, the sense-goddesses ever worship, in the heart-lotus, him — the consciousness-made bliss-bhairava: i praise.",
 brief="Every taste is already a pūjā happening in the heart.",
 logic="Dehastha inverts the usual charge against the senses: the senses are goddesses (indriya-devyāḥ), and their enjoyment of their objects is continuous worship of the Bhairava made of consciousness. Eating is the oldest form of practice — the offering is already being made in the heart-lotus.",
 howto="At the first bite, feel the heart-lotus (just behind the centre of the chest) as the altar and the flavour as the flower landing on it. Three bites only — overdoing it kills the taste. The feeling: gratitude with heat. The sense is honoured as a goddess, not supervised as a thief.",
 source_path="sources/deha-p01.md", source_ref="v.5"),
dict(id="mpa-1", section="wake", title="Homage to the World-Formed",
 source="Mahopadeśaviṃśatikā v.1",
 iast="prapañcottīrṇarūpāya namaste viśvamūrtaye | sadādivyaprakāśāya svātmane'nantaśaktaye",
 en="homage to the form that has crossed beyond the manifest — to the self of the world's form; to the ever-divinely-shining, to the self that is unending power.",
 brief="The first word of the day: bowing to what was here before you woke.",
 logic="Three appositions do the work: he has passed beyond the manifest yet IS the world's form; he always shines with divine light; he is your own self and consists of inexhaustible power. The logic is identity, not distance — you salute the world-form because you address what already shines.",
 howto="Sitting up before your feet touch the floor. Three clauses, three slow bows of the head. Feel the room as svātmane'nantaśaktaye — not out there but as your own body's brightness. Don't visualise a figure; visualise light that has nowhere to go. One round, then stand.",
 source_path="sources/L2-mpa-p01.md", source_ref="v.1"),
dict(id="deha-1", section="wake", title="The Body-Temple Offering",
 source="Dehastha v.1",
 iast="deho devālayaḥ proktaḥ svātmā devaḥ sanātanaḥ | tyajedajñānanirmālyaṃ so'haṃ bhāvena pūjayet",
 en="the body is declared god's temple, the own self the eternal god. casting off the sweepings of ignorance, let him worship with the feeling: i-am-he.",
 brief="The morning rite in one verse: the body is the shrine, so'ham is the worship.",
 logic="Dehastha compresses a whole pūjā into four clauses. Temple, God, sweeping, worship: a temple needs cleaning before its God is honoured, and the 'sweepings of ignorance' are the ordinary assumption that the body is mere matter. The worshipper and the worshipped collapse — so'ham bhāvena, with the feeling I-am-He.",
 howto="Wake and stay horizontal. Sweep an imaginary hand from head to toe three times — that is casting off the sweepings. Then place attention at the heart and let so'haṃ, so'haṃ rest with the breath for twelve rounds. The feeling: warmth at the chest, not a thought — the body as lit. Then rise: the day is the pūjā.",
 source_path="sources/deha-p01.md", source_ref="v.1"),
dict(id="mpa-10", section="wake", title="The Three States as His Rays",
 source="Mahopadeśaviṃśatikā v.10",
 iast="jāgratasvapnasuṣuptyādyā dhārayaṃśca nijāḥ kalāḥ | svecchayā bhāsi naṭavan niṣkalo'si ca tattvataḥ",
 en="waking, dreaming, deep sleep and the rest — you hold them as your own portions. By your will you shine like an actor, yet you are partless in truth.",
 brief="The three states are costumes; the one who shines is partless.",
 logic="The verse splits experience from experiencer: the states are kalāḥ, portions or costumes — things held; the holding is by svecchā, your own will; and the actor is partless though he plays many parts. Play and partlessness are asserted in one breath, so no state can claim you.",
 howto="Recite on waking, naming each state as you come out of it: 'that was a costume.' The actor-idea is literal — you played sleep for seven hours. Feel the partlessness as the fact that nothing about you has edges. Keep it memorised: the fastest exit from a bad dream.",
 source_path="sources/L2-mpa-p01.md", source_ref="v.10"),
dict(id="mpa-11", section="sleep", title="From Your Waking, His Waking",
 source="Mahopadeśaviṃśatikā v.11",
 iast="tvatprabodhāt prabodho'sya tvannidrāto layo'sya yat | atastvadātmakaṃ sarvaṃ viśva sadasadātmakam",
 en="from your waking comes his waking; from your sleep comes his merging. hence all is of your nature — the world, both real and unreal.",
 brief="Your sleep does not stop the world — it feeds it.",
 logic="Two transfers: prabodha (waking) passes from you to him, laya (dissolution) from his sleep to the world. Because his waking enlivens the world and his sleep dissolves it, everything is tvad-ātmaka, of your nature. Sleep is not the end of practice but its most global act: when you sleep you participate in his laya.",
 howto="Last line of the day. Lie down and take one awake minute: you are about to do what he does at night. Don't stay awake doing this — fall asleep inside the thought. Feeling-tip: as the eyes close, feel the day's edges get soft, 'unreal' — that softening is sadasadātmakam. If anxious at night, this dissolves the day rather than reviewing it.",
 source_path="sources/L2-mpa-p02.md", source_ref="v.11"),
dict(id="vbt-75", section="sleep", title="In Sleep, When the Outer Range Perished",
 source="Vijñāna Bhairava v.75",
 iast="anāgatāyāṃ nidrāyām praṇaṣṭe bāhyagocare | sāvasthā manasā gamyā parā devī prakāśate",
 en="in the not-yet-come sleep, when the outer range has perished — that state, to be gone to by mind, the supreme goddess shines forth.",
 brief="The instruction for the moment before sleep: go there by mind.",
 logic="Three conditions: sleep that has not yet arrived; once the outer field has died. In that gap, to be gone to by mind, parā devī, the supreme Goddess, shines — not is-made. The verse locates practice in the dying of the outer senses, where consciousness is neither awake nor asleep, and names what appears there as Śakti herself.",
 howto="At lights-out, on your back, one hand on the belly. Wait for the outer field to fade — sounds go dull, images slow. Then instead of following sleep passively, send the mind as an arrow to the heart-centre, once. Then release. The Goddess-feel is a hum or warmth behind the chest; if images swarm you have grasped — release and let the hum carry. Single-shot: no repetitions.",
 source_path="sources/vbt-p08.md", source_ref="v.75"),
dict(id="sst-9-14", section="sleep", title="At Your Cool Feet", corpus=[9,14],
 source="Utpaladeva, Śivastotrāvalī 9.14",
 en="when will i lie down — free of every object, settled in the embrace of undiminished glory — at your two cool lotus feet?",
 brief="The sleep prayer: the cool feet are the peace after the fever of wanting.",
 logic="Utpaladeva asks when he will lie down free of every object (aśeṣaviṣaya — no grasping left), settled in undiminished glory (aśūnya śrī), at the two cool lotus feet (śītāṅghri-kuśeśaya). 'Free of every object' is not blankness but the rest that remains when the mind stops reaching. The cool feet are the peace of Śiva.",
 howto="In bed. Say it once, then let the image of the two cool feet form under the mind's eye — no details needed, just the coolness. The feeling to find: the fever of the day dropping. If the mind races, return to the coolness, not the words.",
 source_path="sources/sivastotravali_corpus.json", source_ref="9.14"),
dict(id="sst-16-8", section="wait", title="I Don't Mind", corpus=[16,8],
 source="Utpaladeva, Śivastotrāvalī 16.8",
 en="in crisis or at ease, weeping or laughing, grave or unhinged — by devotion, lord, let me be so.",
 brief="The api-chain refuses resolution: everything is allowed.",
 logic="The verse piles up opposites with 'api' (even): viṣama/sthāna (crisis/peace), rudann/hasann (weeping/laughing), gambhīro/vicitta (grave/unhinged). Devotion is not the absence of any of them; it is what holds them. The prayer does not ask for calm — it asks to be devotion through whatever arrives.",
 howto="Use it when waiting has turned into agitation — a queue, a delay, a message that won't come. Say it once inwardly. Don't wait for composure: the very mess is the place where devotion can be. Feeling-tip: the shoulders drop half a millimetre; that's the api doing its work.",
 source_path="sources/sivastotravali_corpus.json", source_ref="16.8"),
dict(id="sst-17-19", section="wait", title="In Every Action", corpus=[17,19],
 source="Utpaladeva, Śivastotrāvalī 17.19",
 en="o lord, may i experience, moment by moment, in every action, the great joy of drinking the nectar of your worship.",
 brief="The in-between moment becomes the practice itself.",
 logic="Utpaladeva prays for the taste of worship inside every action — not more ritual, but the nectar of pūjā in the ordinary. 'Moment by moment' (kṣaṇāt kṣaṇam) is the whole method: the repeated return of attention. Waiting is full of kṣaṇas — this verse makes them the site of the drink.",
 howto="At any transition or pause: say it once, then take one breath as if that breath were the nectar. Don't manufacture joy — notice the small lift that a pause already gives. Three pauses, three sips, and the waiting has changed colour.",
 source_path="sources/sivastotravali_corpus.json", source_ref="17.19"),
dict(id="bh-5", section="negative", title="I Never Fear", source="Abhinavagupta, Bhairavastava 5",
 iast="ittham upoḍhabhavanmayasaṃviddīdhitidāritabhūritamisraḥ | mṛtyuyamāntakakarmapiśācair nātha namo'stu na jātu bibhemi",
 en="thus, with the great darkness torn open by the rays of the consciousness become you — lord, namas; i never fear, not from death, from yama, from the ender, from the ghosts of karma.",
 brief="Fearlessness as salutation, not as courage.",
 logic="Awareness has already torn the darkness; what remains is not courage but salutation. The devotee still names death's ministers — Mṛtyu, Yama, the ender, the karma-ghosts — and bows to them, because they too are Śiva's play. 'I never fear' is the natural temperature of recognition.",
 howto="Recite when fear arrives — not to banish it but to salute it. The fear is named, bowed to, and left standing. Feeling-tip: the chest opens rather than tightens; the bow is physical as well as verbal. Do it at night, or in the moment before the difficult thing.",
 source_path="sources/bhairavastava.md", source_ref="bh-p05"),
dict(id="bh-3", section="sick", title="No Fear-Talk", source="Abhinavagupta, Bhairavastava 3",
 iast="svātmani viśvagaye tvayi nāthe tena na saṃsṛtibhītikathāsti | satsv api durdharaduḥkhavimohatrāsavidhāyiṣu karmagaṇeṣu",
 en="with you as lord, all-pervading in own self — therefore no talk of transmigration-fear. even though hard-to-bear suffering, delusion, terror-causing karma-hosts are present.",
 brief="The suffering is conceded; the fear-talk is not.",
 logic="The verse does not deny suffering — it concedes the karma-hosts (durdharaduḥkhavimohatrāsavidhāyiṣu) — but denies the fear of saṃsāra, because the Lord is all-pervading in the self. Suffering can be present without being feared; the fear-talk is what stops.",
 howto="When negative, say it and let the concession stand: yes, this is hard; and the fear of it is separate from the pain itself. The verse splits them. Feeling-tip: the pain stays, the story about the pain thins. That thinning is the verse working.",
 source_path="sources/bhairavastava.md", source_ref="bh-p03"),
dict(id="pan-4", section="negative", title="The Cloud Lifts", source="Abhinavagupta, Pañcaślokī 4",
 iast="gurorvākyādyukti-pracaya-racana-unmārjana-vaśātsamāśvāsācchāstraṃ prati samucitādapi kathitam | vilīne śaṅkābhre hṛdayagaganodbhāsimahasaḥ prabhoḥ sūryasyeva spṛśatu caraṇān dhvāntajayinaḥ",
 en="from the guru's word — by the force that wipes away the fabric of heaped-up reasonings — and from the assurance told, fittingly, out of regard for scripture: when the cloud of doubt has dissolved, let me touch the feet of the lord, whose splendor shines in the sky of the heart — like the sun, the conqueror of darkness.",
 brief="For doubt: the cloud dissolves, the sun is already there.",
 logic="The verse traces doubt to 'heaped-up reasonings' (pracaya-racana) that the guru's word wipes away, and promises that when the cloud of doubt (śaṅkābhra) dissolves, the feet of the sun-like Lord — shining in the heart-sky — become touchable. Doubt is weather, not the sky.",
 howto="When doubt is heavy, say it and picture the cloud as literal weather over the heart. The sun is not summoned; it is uncovered. Feeling-tip: the image of touching the feet — a small act of trust — is the whole practice. Repeat the last line as a refrain.",
 source_path="sources/pancashloki.md", source_ref="pan-p04"),
dict(id="svab-6", section="negative", title="The Knife That Cuts the Knot",
 source="Svabodhasiddhi v.6",
 iast="mamāham iti hṛdgranthicchedanaikakṛpāṇikām | spandāspandakṛtagrāsāṃ naumy ahaṃ śuddhasaṃvidam",
 en="i bow — i — to pure awareness: the knife that alone cuts the heart's knot of 'mine' and 'i', the one that has swallowed both the throb and its stillness.",
 brief="For guilt and possessiveness: one cut, and the knot is gone.",
 logic="The knot (granthi) is mamāham — 'mine' and 'I', two threads. The instrument is a kṛpāṇa, a knife, and only one does it: pure awareness. And the knower's own domain — throb and stillness — has already been swallowed by that knife. 'I bow — I' stages the surrender: the pronoun survives long enough to bow, then is cut too.",
 howto="Recite with a hand flat over the sternum. Weight the first aham: feel where your 'I' sits in the body, and on 'naumy ahaṃ' press gently and let that place soften. The image is a blade, but the feeling is a release of grip, not a strike — knots untie. Fastest on small knots (a slighted email), slower on old ones.",
 source_path="sources/L2-svab-p01.md", source_ref="v.6"),
dict(id="pan-2", section="positive", title="Victory at the Door", source="Abhinavagupta, Pañcaślokī 2",
 iast="maheśa tvaddvāri sphuratu rucirā vāg atitarāṃ mama eṣā nirdoṣaṃ jaya jaya maheśeti satatam | śivā saiṣā vāṇī bhavatu śivadā mahyam aniśaṃ maheśanāthaṃ māṃ śaraṇada sanāthaṃ kuru vibho",
 en="o maheśa, may this lovely speech of mine flash forth at your door, faultlessly, again and again: victory, victory to maheśa! may this auspicious speech be giver of bliss to me, unceasingly. o lord, o giver of refuge, make me — whose protector is maheśanātha — to have a protector.",
 brief="The prayer of rejoicing: only speech to offer, and it flashes at the door.",
 logic="The devotee has nothing but speech, and asks that it flash at the Lord's door, faultless, repeating 'victory, victory to Maheśa'. Then the real request: make me to have a protector. Śaraṇāgati is not becoming strong but being held — and the rejoicing is the holding already underway.",
 howto="When something good has happened — or when you want to rejoice anyway — say it aloud if possible. The repetition of 'jaya jaya maheśa' is the celebration. Feeling-tip: the smile arrives before the words; let it. The verse is permission to be happy in his name.",
 source_path="sources/pancashloki.md", source_ref="pan-p02"),
dict(id="sst-1-5", section="positive", title="Mad with the Nectar of Devotion", corpus=[1,5],
 source="Utpaladeva, Śivastotrāvalī 1.5",
 en="victory to those who have become mad by taking the nectarized liquor of thy devotion — those who, though alone, are always with thee, though without a second.",
 brief="Devotion as intoxication: the positive state has a name.",
 logic="The verse names the ones who have drunk bhakti-rasa (devotion's nectar) and gone mad (unmadāḥ) — and their sign: though apparently alone, they are always with him; though without a second, they are not lonely. The 'madness' is the joy that comes from drinking the right thing.",
 howto="When the joy is already there, say it and name it: this is the nectar. Don't analyse the joy; toast it. Feeling-tip: the slight giddiness the verse describes is the actual state — lean into it, don't explain it to anyone.",
 source_path="sources/sivastotravali_corpus.json", source_ref="1.5"),
dict(id="spanda-1", section="positive", title="The Wheel of Powers",
 source="Vasugupta, Spandakārikā 1.1",
 iast="yasyonmeṣanimeṣābhyāṃ jagataḥ pralayodayau | taṃ śakticakravibhavaprabhavaṃ śaṅkaraṃ stumaḥ",
 en="to him by whose opening and closing the world dissolves and arises — to śaṅkara, source of the glory of the wheel of powers, we sing.",
 brief="The opening hymn: the world blinks, and we sing to the one who blinks it.",
 logic="The Spandakārikā opens with a hymn to the pulse: by the Lord's opening and closing (onmeṣa-nimeṣa — his blink) the world dissolves and arises. The 'wheel of powers' is the circle of śaktis through which consciousness manifests. To sing is to join the pulse rather than resist it.",
 howto="Recite when the world feels vivid — when colours are sharp, when music lands, when the pulse is obvious. It's a song of participation. Feeling-tip: blink with the verse; the world dissolving and arising on each blink is literal enough.",
 source_path="sources/spanda.md", source_ref="Spandakārikā 1.1"),
dict(id="mpa-20", section="work", title="Yoke the Mind",
 source="Mahopadeśaviṃśatikā v.20",
 iast="evameva parā pūjā sarvāvasthāsu sarvadā | aikyabuddhayā tu sarveśe mano deve niyojayet",
 en="just so is the highest worship — in every state, at all times: with a mind of oneness, one should yoke the mind to god as the lord of all.",
 brief="The instruction after the litany: work is the highest pūjā.",
 logic="Parā pūjā is ritual re-specified: all states, all times instead of the fixed occasion, and aikyabuddhi — oneness-mindedness — instead of the duality of giver and gift. The verb is niyojayet, yoke: the mind is a draught-animal that must be hitched, and the yoke is identity. The desk becomes the temple by the hitching, not the décor.",
 howto="Before opening the laptop: one line, then begin. The test for aikyabuddhi: the boundary of your skin thins. If it sharpens, you're thinking oneness, not yoking it — drop to the breath and restart. Each task is one yoke; re-hitch as often as needed.",
 source_path="sources/L2-mpa-p02.md", source_ref="v.20"),
dict(id="sst-1-14", section="work", title="Achieve God in Activity", corpus=[1,14],
 source="Utpaladeva, Śivastotrāvalī 1.14",
 en="so the devotee is told: become śiva and worship. you yourself are the essence of the body, purified by devotion's non-duality.",
 brief="Lakshmanjoo's work verse: find God in the activity, not by shunning it.",
 logic="The verse (śivo bhūtvā yajeti) instructs: become Śiva and worship — and adds that the body's essence (vapuḥ sāraṃ) is refined by bhakti's advaya, non-duality. The gloss from the Academy: achieve God in the activity of the universe, not by shunning it; perceive him in each and every action of life. Work is the field, not the obstacle.",
 howto="At the desk, when work feels like a distraction from practice: say it and reclassify. The spreadsheet, the email, the conversation — that is the worship. Feeling-tip: the task itself becomes slightly luminous; do it as offering, not as interruption.",
 source_path="sources/sivastotravali_corpus.json", source_ref="1.14"),
dict(id="deha-8", section="work", title="I-Making Flowers",
 source="Dehastha v.8",
 iast="kurute bhairavapūjāmanaladalasthā'bhimānakusumairyā | nityamahaṅkṛtirūpāṃ vande tāṃ śāmbhavīmambām",
 en="who performs bhairava's worship, standing in fire's petal, with flowers of i-making — ever of i-making form, i praise her, the mother śāmbhavī.",
 brief="Hand the work-ego over: the ahaṃkāra is the offering.",
 logic="Śāmbhavī stands in the petal of fire and worships with abhimāna-kusuma — flowers of I-making: the sense of mine and I that is normally the problem. The rite converts the fault into the flower. At work, the 'I' that wants credit is not suppressed — it is picked and placed in the fire.",
 howto="When the ego flares mid-task — pride, irritation at the colleague, hunger for recognition: see it as a flower, pick it, place it at the heart's fire. Three flowers are enough. Feeling-tip: relief, like putting down a bag; the fire (warmth at the solar plexus) confirms it.",
 source_path="sources/deha-p01.md", source_ref="v.8"),
dict(id="mpa-9", section="work", title="When Your Form Expands",
 source="Mahopadeśaviṃśatikā v.9",
 iast="tvatsvarūpe jṛmbhamāṇe tvaṃ cāhaṃ cākhilaṃ jagat | jāte tasya tirodhāne na tvaṃ nāhaṃ na vai jagat",
 en="when your own form expands — you and i and the whole world. when its withdrawal is born — neither you, nor i, nor indeed the world.",
 brief="Expansion and withdrawal: the world is his inhale and exhale.",
 logic="Two movements: when svarūpa expands (jṛmbhamāṇe), you, I and the whole world appear together; when it withdraws (tirodhāne), none of the three remains. The verse relativises the entire workday — deadlines, colleagues, the self doing them — as one expansion of his form. Not nihilism: the expansion is real, and so is who expands it.",
 howto="Use it at the overwhelm point — too much to do, the self tightening. Say it and feel the day as one exhale of a larger form. The overwhelm thins because the 'me' carrying it is part of the expansion, not its owner. Then return to the next small task.",
 source_path="sources/L2-mpa-p01.md", source_ref="v.9"),
dict(id="bhair-7", section="social", title="The Speech-Goddess",
 source="Bhairavānukaraṇa v.7",
 iast="svātmaprabhāṃ vidhāya vāgdevīṃ viṣayakusumakḷptārcaḥ | prathamonmeṣaṃ gurum atha vanditvā hṛdayam āviśya",
 en="having made the speech-goddess one's own light, with sense-flowers arranged as offering — bowing to the guru, first unfolding, then entering the heart.",
 brief="Before you speak: make vāk the light, not the weapon.",
 logic="The verse sequences the art of speech: svātmaprabhāṃ vidhāya vāgdevīṃ — make the speech-goddess your own light; arrange the sense-flowers as the offering; bow to the guru, the first unfolding (prathamonmeṣa); then enter the heart. Speech is not emitted from the mouth but lit from the heart and offered with the senses.",
 howto="Before a difficult conversation, a speech, a message you'll regret: one breath, hand on the throat. Make the speech a light — not a blade. Offering the sense-flowers means: don't weaponise what you've seen and heard. Then speak from the heart-entered place, not the throat.",
 source_path="sources/bhairavanukarana.md", source_ref="bhair-p01 v.7"),
dict(id="anu-3", section="social", title="Every Sound Is Mantra",
 source="Anubhavanivedana v.3",
 iast="śabdaḥ kaścana yo mukhādudayate mantraḥ sa lokottaraḥ saṃsthānaṃ sukhaduḥkhajanmavapuṣo yatkāpi mudraiva sā | prāṇasya svarasena yatpravahaṇaṃ yogaḥ sa evādbhutaḥ śāktaṃ dhāma paraṃ mamānubhavataḥ kinnāma na bhrājate",
 en="whatever sound arises from the mouth — that mantra is transcendent. whatever posture of the pleasure-pain-born body — that indeed is mudrā. whatever flowing of breath by its own rhythm — that indeed is wonderful yoga. the supreme śākta abode — while i experience, what indeed would not shine?",
 brief="Every word out of your mouth is already a mantra. Use that.",
 logic="Abhinavagupta's experience-report: any sound from the mouth is lokottara mantra — transcendent; any posture is mudrā; any breath-flow by its own rhythm is yoga. Nothing needs to be Sanskritic to be practice. The verse abolishes the distinction between talking and chanting, fidgeting and ritual, breathing and kriyā.",
 howto="Use it after you've said something — ordinary, even stupid. That was mantra. The recognition flips the whole day: the meeting, the small talk, the complaint — all of it is mantra, mudrā, yoga, shining. Feeling-tip: the mouth becomes a temple; be careful what you put on the altar.",
 source_path="sources/anubhavanivedana.md", source_ref="anu-p03 v.3"),
dict(id="mpa-8", section="social", title="Enough of Difference-Talk",
 source="Mahopadeśaviṃśatikā v.8",
 iast="alaṃ bhedānukathayā tvadbhaktirasacarvaṇāt | sarvamekamidaṃ śāntamiti vaktuṃ ca lajjate",
 en="enough of difference-talk — chewing the sap of devotion to you: all this is one, at peace; and even to say so feels shy.",
 brief="Knowing when to stop talking: the oneness embarrasses speech.",
 logic="Bheda-anukathā, the narration of difference, is abandoned mid-chewing of bhakti-rasa: all is one, at peace. And even to say so feels shy (lajjate) — the verse guards non-duality from becoming a thesis. The oneness is so ordinary that stating it out loud is like announcing a family is at peace: true, and slightly vulgar.",
 howto="Use it when an argument about views has you mid-sentence — or when you're about to explain your practice to someone who doesn't need it. Stop. The shyness is the right register. Feeling-tip: looking away slightly, a small heat in the face — let the body do the disarming.",
 source_path="sources/L2-mpa-p02.md", source_ref="v.8"),
dict(id="mpa-14", section="bath", title="What Bath for the Stainless?",
 source="Mahopadeśaviṃśatikā v.14",
 iast="nirmalasya kutaḥ snānaṃ vastraṃ viśvodarasya ca | nirlepasya kuto gandho ramyasyābharaṇaṃ kutaḥ",
 en="for the stainless, what bath? for the world-bellied, what garment? for the unanointed, what scent? for the lovely, what jewel?",
 brief="Shower, towel, scent, jewel — all addressed to one who needs none.",
 logic="The litany names the bathroom itself: snāna (bath), vastra (garment), gandha (scent), bharaṇa (jewel) — each with a deity stripped of the lack it serves: stainless, world-bellied (all-containing), unanointed, lovely. What looks like futility is the precise applicability of each gift: you bathe the unblemished because bathing is what love does, not what dirt requires.",
 howto="In the shower: name each item as you use it — water for the stainless, towel for the world-bellied, scent for the unanointed. The mismatch is the smile. Feeling-tip: the water becomes an offering rather than a chore; three items, three small bows.",
 source_path="sources/L2-mpa-p02.md", source_ref="v.14"),
dict(id="sst-17-26", section="bath", title="This Body for Worship", corpus=[17,26],
 source="Utpaladeva, Śivastotrāvalī 17.26",
 en="may this body of mine — nourished by the clear, bright nectar of devotion rising within — be fit only for your worship.",
 brief="The body leaves the water consecrated: today's uniform is worship.",
 logic="The body is not renounced; it is consecrated. Nourished by the clear nectar of devotion rising in the heart (antar ullasad acchāccha-bhakti-pīyūṣa), it becomes fit for pūjā — and then it is the offering itself. This is the Trika answer to body-denial: the body is the Lord's instrument, and devotion makes it luminous.",
 howto="Dressed, before leaving the bathroom: say it once and feel the freshly washed body as anointed rather than merely clean. The day ahead is the pūjā; the body is the instrument. Feeling-tip: a slight uprightness in the spine — the instrument picking itself up.",
 source_path="sources/sivastotravali_corpus.json", source_ref="17.26"),
dict(id="deha-6", section="wake", title="The Play of the Dawning",
 source="Dehastha v.6",
 iast="udayāvabhāsacarvaṇalīlāṃ viśvasya yā karotyaniśam | ānandabhairavīṃ tāṃ vimarśarūpāmahaṃ vande",
 en="the play of the dawning, shining forth, and chewing over of the universe, which she performs unceasingly — bliss-bhairavī, her, whose form is reflection, i praise.",
 brief="The dawn is her play: she chews the universe into light, unceasingly.",
 logic="Bhairavī's līlā is udaya-avabhāsa-carvaṇa — the dawning, shining and chewing of the universe, performed without pause; her form is vimarśa, reflective awareness. The morning light is not physics but her appetite: she is already chewing the day into being when you open your eyes.",
 howto="At first light, before anything else: watch the room brighten and name it her chewing. One line. Feeling-tip: the day is being eaten into existence for you; you arrive mid-meal. Gratitude, not effort.",
 source_path="sources/deha-p01.md", source_ref="v.6"),
dict(id="mpa-17b", section="bath", title="Waving-Lights for the Self-Shining",
 source="Mahopadeśaviṃśatikā v.17",
 iast="svayaṃ prakāśamānasya kuto nīrājanaṃ vibhoḥ | vedavācāmavedyasya kutaḥ stotraṃ vidhīyate",
 en="whence waving-lights for the self-shining lord? how is a hymn enjoined for him whom the veda cannot say?",
 brief="The mirror, the lamp: he lights himself — so the light is for you.",
 logic="Two paradoxes: an offering of light presupposes darkness in the recipient; speech presupposes an object speech can reach. The Lord is self-lit and beyond the Veda's words. The rite's use falls on the offerer — you wave the lamp so your own eyes open; you sing because the singing lights you.",
 howto="At the bathroom mirror, hand raised with the light: you are the lamp-bearer, and the face that brightens is the audience. Hum, don't articulate — you have just honoured the Vedavācāmavedya. Feeling-tip: the chest brightens before the mirror does.",
 source_path="sources/L2-mpa-p02.md", source_ref="v.17"),
dict(id="mpa-19b", section="bath", title="Pardon for the Unseen",
 source="Mahopadeśaviṃśatikā v.19",
 iast="pūrṇasya dakṣiṇā kutra nityatṛptasya tarpaṇam | visarjanaṃ vyāpakasyā'pratyakṣasya kṣamāpaṇam",
 en="where is the fee for the full? libation for the ever-content? dismissal for the all-pervading? pardon for the unseen?",
 brief="The ritual closes with forgiveness — and no account to settle.",
 logic="The four closing rites: dakṣiṇā (fee), tarpaṇa (libation), visarjana (dismissal), kṣamāpaṇa (apology for faults) — all presuppose want, debt, departure and fault in one who is full, content, all-pervading and unseen. The kṣamāpaṇa for the apratyakṣa flips apology into recognition: you apologise to what was never absent.",
 howto="Use it at the end of the bath as the day's closing already: one bow, weight the last word — pardon. The feeling is the end of accounting: no tally of errors, no debt. Guilt arrives, is named as one of the litany's items, and dissolves with the god it expected to offend.",
 source_path="sources/L2-mpa-p02.md", source_ref="v.19"),
dict(id="pan-3", section="social", title="When Your Words Are Not Heard",
 source="Abhinavagupta, Pañcaślokī 3",
 iast="brūṣe nottamāṅga paśyasi na māmetādṛśaṃ duḥkhitaṃ vijñaptiṃ bahudhā kṛtāṃ na śṛṇuṣe nāyāsi manmānase | saṃsārārṇavagartamadhyapatitaṃ prāyeṇa nālambase vākcakṣuḥśravaṇāṅghriṇādirahitaṃ tvāmāha satyaṃ śrutiḥ",
 en="you speak not, o best-limbed one; you look not upon me, wretched as i am. my entreaty, made in many ways, you hear not; you come not into my mind. fallen amid the pit of the ocean of transmigration, i am mostly left unsupported — yet scripture truly declares you devoid of speech, sight, hearing, feet and the like!",
 brief="The complaint: you don't speak, look or hear — and scripture says you can't. Ouch.",
 logic="Pañcaślokī 3 is the reproach: the devotee accuses Śiva of silence — no speech, no glance, no listening, no arrival in the mind — then undercuts himself with scripture's own claim that the Lord is devoid of speech, sight, hearing and feet. The complaint and the theology cancel: you're angry at a god who, by definition, never had a mouth to answer with.",
 howto="Use it when you've spoken and nobody heard — human or divine. Say the whole complaint with feeling; the scripture-clause at the end is the punchline that dissolves it. Feeling-tip: the irritation turns to laughter mid-verse; that laugh is the prasāda.",
 source_path="sources/pancashloki.md", source_ref="pan-p03"),
dict(id="sst-15-2", section="food", title="Devouring Māyā as Food", corpus=[15,2],
 source="Utpaladeva, Śivastotrāvalī 15.2",
 en="o nātha, your devotees roam happy on the shore of the world, filled and satisfied by consuming māyā, time, fate and desire themselves.",
 brief="The devotee's menu: māyā, time, niyati, desire — eaten for breakfast.",
 logic="The verse is a mealtime paradox: the devotees are tarpitāḥ, sated, by consuming māyīya, kāla, niyati, rāgādi — the very forces that starve everyone else. What the world treats as hunger (desire, fate, time) is their food. They roam happy on the shore of the world, having eaten the ocean.",
 howto="Before or after a meal, when desire is loudest: name it as the course — māyā, time, fate, desire — and eat it. The hunger is the menu. Feeling-tip: the wanting transforms into satedness mid-sentence; that flip is the verse working.",
 source_path="sources/sivastotravali_corpus.json", source_ref="15.2"),
dict(id="anu-2b", section="wait", title="Abandon Nothing, Grasp Nothing",
 source="Abhinavagupta, Anuttarāṣṭikā v.2",
 iast="saṃsāro 'sti na tattvatas tanubhṛtāṃ bandhasya vārtaiva kā bandho yasya na jātu tasya vitathā muktasya muktikriyā | mithyāmohakṛd eṣa rajjubhujagacchāyāpiśācabhramo mā kiṃcit tyaja mā gṛhāṇa vihara svastho yathāvasthitaḥ",
 en="saṃsāra is not, in truth, for body-holders — of bondage, what news? bondage never truly is for anyone — so for the free, liberation-rite is false. this error-maker is rope-snake-shadow-ghost-delusion. abandon nothing; grasp nothing; live healthy, staying as you are.",
 brief="The waiting instruction par excellence: don't add, don't subtract, just stay.",
 logic="The verse dismantles bondage itself — saṃsāra never truly was; the bondage-story is the rope-snake-shadow ghost of māyā. Then the instruction in four beats: mā kiṃcit tyaja (abandon nothing), mā gṛhāṇa (grasp nothing), vihara (live), svastho yathāvasthitaḥ (stay as you are). Waiting is where the mind most wants to add or subtract.",
 howto="In the queue, the delay, the silence: say the last line — 'live healthy, staying as you are.' The restlessness wants to grab something or drop something; the verse forbids both. Feeling-tip: the hands open and close once, then rest; the waiting is now the living.",
 source_path="sources/anuttarastika.md", source_ref="anu-p02 v.2"),
dict(id="sst-16-1", section="wait", title="Two Classes of People", corpus=[16,1],
 source="Utpaladeva, Śivastotrāvalī 16.1",
 en="there are two classes found in this universe: one class is of ordinary people, and another are those who are thy devotees.",
 brief="In the queue: two kinds of people, and you know which you are.",
 logic="The verse is a quiet census — only two classes, ordinary folk and bhaktas — with no third category of the merely interested. It's a wry re-classification of the crowd: everyone waiting with you belongs to one of two groups, and the difference isn't visible from the outside. The devotee smiles at the census.",
 howto="Use it in any crowd — the queue, the train, the meeting. Run the census once: two classes. Then check which one is noticing the census. Feeling-tip: a small private smile; nobody can tell from the outside which class you're in — that's the point.",
 source_path="sources/sivastotravali_corpus.json", source_ref="16.1"),
dict(id="bh-4", section="negative", title="Turn Not This Wrathful Gaze",
 source="Abhinavagupta, Bhairavastava 4",
 iast="antaka māṃ prati mā dṛśam enāṃ krodhakarālatāṃ vinidhehi | śaṅkarasevanacintanadhīro bhīṣaṇabhairavaśaktimayo 'smi",
 en="o ender, turn not toward me this most wrathful-terrible gaze. by śaṅkara-service, contemplation-firm, i am terrifying-bhairava-power-filled.",
 brief="Facing wrath — his or theirs — without flinching.",
 logic="The devotee does not ask the wrath away; he asks that it not be aimed at him, and answers with his own composition: service and firm contemplation have made him bhīṣaṇa-bhairava-śakti-maya, filled with the terrifying power itself. You cannot be burned by the fire you are made of. The gaze turns aside because there is no separate target left.",
 howto="When facing anger — a boss, a partner, your own — say it with the hand on the sternum. Don't argue with the wrath; declare your composition. Feeling-tip: you become too made-of-it to be its victim; the gaze slides off because the target dissolved.",
 source_path="sources/bhairavastava.md", source_ref="bh-p04"),
dict(id="anu-8b", section="positive", title="Enjoy Lordhood",
 source="Abhinavagupta, Anuttarāṣṭikā v.8",
 iast="yat satyaṁ yad asatyam alpabahulaṁ nityaṁ na nityaṁ ca yat yan māyāmalinaṁ yad ātmavimalaṁ ciddarpaṇe rājate | tat sarvaṁ svavimarśasaṁvidudayād rūpaprakāśātmakaṁ jñātvā svānubhavādhirūḍhamahimā viśveśvaratvaṁ bhaja",
 en="whatever is real and whatever is unreal, little or much, eternal or not; whatever shines stained by māyā or pure as the self in the mirror of consciousness — know it all to be the light of form arising from one's own self-awareness; then, with a glory mounted on your own experience, enjoy the lordhood of the universe.",
 brief="The last verse of the Anuttarāṣṭikā: enjoy Lordhood.",
 logic="The verse gathers the whole world — real, unreal, stained, pure — into the mirror of consciousness as the light of form arising from one's own awareness. Then the instruction: bhaja viśveśvaratvam, enjoy the Lordhood of the universe. Lordhood is not power over things; it is the taste of seeing them as yourself. This is rejoicing as a metaphysical claim.",
 howto="When things are going well — or when you want to rejoice anyway: say the last clause aloud. Lordhood is a tasting, not a trophy. Feeling-tip: the chest opens, the world turns slightly luminous; that luminance is svānubhavādhirūḍha, mounted on your own experience. Don't explain it to anyone.",
 source_path="sources/anuttarastika.md", source_ref="anu-p08 v.8"),
dict(id="anu-4b", section="sleep", title="Bliss Is the Forgotten Treasure",
 source="Abhinavagupta, Anuttarāṣṭikā v.4",
 iast="ānando 'tra na vittamadhyamadavan naivāṅganāsaṅgavat dīpārkendukṛtaprabhāprakaravan naiva prakāśodayaḥ | harṣaḥ saṃbhṛtabhedamuktisukhabhūr bhārāvatāropamaḥ sarvādvaitapadasya vismṛtanidheḥ prāptiḥ prakāśodayaḥ",
 en="bliss here is not wealth-middle-intoxication, nor like enjoying women, nor lamp-sun-moon-made splendour-multitude — and not the light-rise either. joy with gathered-difference-liberation-bliss-ground, like burden-lowering, is the attainment of the forgotten treasure of the all-nonduality state — the light-rise.",
 brief="The sleep verse: bliss as burden-lowering, the forgotten treasure.",
 logic="The verse defines bliss by negation — not wealth-drunkenness, not sensual pleasure, not spectacle-light — then gives the positive: harṣa like bhārāvatāra, the lowering of a burden, is the prāpti of vismṛta-nidhi, the forgotten treasure of the non-dual state. Falling into sleep is that burden-lowering: the day's weight set down at the door.",
 howto="In bed, say it and feel the day's weight as the literal bhāra being lowered. Bliss here is not an event but an unloading. Feeling-tip: the shoulders drop a centimetre deeper each line; by the last line the bed has the treasure under it.",
 source_path="sources/anuttarastika.md", source_ref="anu-p04 v.4"),
# ---------------- SICK ----------------
dict(id="pan-5", section="sick", title="Forgetting, and the Final Plea",
 source="Abhinavagupta, Pañcaślokī 5",
 iast="yātastvatsahavāsato bahutaraḥ kālo vatāsmin kṣaṇe kiṃ kiṃ vā na kṛtaṃ tvayā varagurūpāsānimittena me | vāraṃ vāramahaṃ punarnirupamāṃ divyaṃ bhuvaṃ prāsuvatkāyastvāṃ kila vismarāmi yadataḥ stheyaṃ na bhūyastvayā",
 en="much time dwelling with you has passed — alas, in this very moment! what, what has not been done by you for me, for the sake of serving the excellent guru! again and again i, whose body has attained the incomparable divine plane — yet indeed i forget you. therefore, by you let there be no further staying-away!",
 brief="The illness plea: you've done everything for me — so don't stay away now.",
 logic="Pañcaślokī 5 turns on time and forgetting: much time has passed with him; nothing has not been done for you; and still you forget him. The plea — let there be no further staying-away — is asked not from desert but from a record of grace: you owe nothing, he has paid everything, so his absence now would be the only unkindness left.",
 howto="When ill and feeling forgotten: say the whole verse as the complaint it is — 'what has not been done by you for me?' — and let the last line be the request. Feeling-tip: the forgetting is admitted first (you forgot him); the plea is fair because of that. One round, then rest.",
 source_path="sources/pancashloki.md", source_ref="pan-p05"),
dict(id="sst-5-2", section="sick", title="Dance with the Foot-Dust", corpus=[5,2],
 source="Utpaladeva, Śivastotrāvalī 5.2",
 en="when will that glorious day come to me, my lord — your lotus-foot dust anointing my hair — that i may dance the dance begun from the endless?",
 brief="For the sickbed: the day I dance with your foot-dust on my head.",
 logic="The verse is pure longing — kadā, when: when will my hair be rubbed with the dust of your lotus feet, and I dance a dance begun from the boundless? The foot-dust is the classical sign of total surrender — the head as the lowest place, the master's foot as the highest — and the dance is what follows: not recovery as return to normal, but entry into a dance that starts at the infinite.",
 howto="From the sickbed, say it as a question — kadā, when — without demanding the answer today. Picture only the dust on the hair; the dance can wait. Feeling-tip: longing itself becomes the posture; the verse sanctifies not-yet.",
 source_path="sources/sivastotravali_corpus.json", source_ref="5.2"),
dict(id="mpa-3", section="sick", title="Whatever Is Seen Is You",
 source="Mahopadeśaviṃśatikā v.3",
 iast="antardehe mayā nityaṃ tvamātmā ca gaveṣitaḥ | na dṛṣṭastvaṃ nacaivātmā yacca dṛṣṭaṃ tvameva tat",
 en="inside the body, sought by me always — you as self, and the self is never seen. whatever is seen is you alone, that.",
 brief="When the body hurts: whatever is seen — even this — is you.",
 logic="The verse performs a swap: I search for you inside the body as the self, and the self is never seen — but whatever IS seen, tvameva tat, is you alone. Applied to illness: the pain, the weakness, the scanned body — none of it is the self, and all of it is him. The sick body becomes the visible half of an invisible lord.",
 howto="When pain or weakness is present: look at it once — the ache as an object — and name it 'seen: you.' Not as denial of pain but as address change. Feeling-tip: the pain stays but loses its claim to be yours; it's his visible side, and visibility is already grace.",
 source_path="sources/L2-mpa-p01.md", source_ref="v.3"),

# ---------------- CHANTED AT THE SANGHA (Swami Lakshmanjoo) ----------------
dict(id="aghora", section="sangha", title="The Aghora Mantra",
 source="Yajurveda · chanted by Swami Lakshmanjoo at every Weekly Sangha",
 iast="aghorebhyo 'tha ghorebhyo ghoraghoratarībhyaśca | sarvataḥ śarva sarvebhyo namaste rudrarūpebhyaḥ ||",
 en="salutations to aghora, to ghora, to ghoraghora-tarī — to sarva in all directions, to all the rudra-forms: namas.",
 brief="The Sangha's opening chant. Swamiji's directive after his 1989 vision: spread this message all over the world.",
 logic="The verse salutes the three energies of Rudra as his forms. Per Swamiji's Tantrāloka 3.257-259 teaching: Aghorā carries you to God-consciousness at once, even without your wish (cit-śakti); Ghorā makes the desirer wait — 'don't hurry, just we will see the time' (icchā-śakti); Ghoratarī carries the careless downward (jñāna-śakti). The protection invoked is real but conditional: Svacchandanātha's eighteen arms are the eighteen tattvas, outgrowths of the five śaktis, made for the protection of the individual — but protection requires the yamas and niyamas, the supreme of which is īśvara-praṇidhāna: if you love Lord Śiva and are devoted to Him, it is not possible for Him to neglect you.",
 howto="Chant it where Swamiji put it: at the opening of any practice — this is the beginning of the Weekly Sangha. Three to nine rounds, aloud. When to: first thing in the morning, or at any moment of fear — you are addressing the three energies directly. Effect, per the tradition he taught: protection through the eighteen arms and purification of the three channels, body, speech and mind. His own instruction for its spread: 'You should spread this message all over the world.'",
 source_path="sources/efficacy-aghora.pdf", source_ref="Secret Supreme ch.13 · letter 1989"),
dict(id="bahurupa-core", section="sangha", title="The Secret Remedy",
 source="Śrī Bahurūpa-Garbha Stotra, Bhairava's answer (vv.5-7)",
 iast="śṛṇu devī! paraṁ guhyaṁ rahasyaṁ paramādbhutam | sarva-pāpa-praśamanaṁ sarva-duḥkha-nivāraṇam || prāyaścitteṣu sarveṣu tīvreṣv api vimocanam | sarva-cchidrāpa-haraṇaṁ sarvārti-vinivārakam || samayolaṅghane ghore japādeva vimocanam | bhoga-mokṣha-pradaṁ devī! sarva-siddhi-phalapradam ||",
 en="listen, goddess: the supreme secret, most wonderful — it pacifies all sins, removes all sorrows; releases even from intense atonement, removes every gap, uproots all affliction; in the breaking of the vows the remedy is the recitation alone — it grants enjoyment and liberation, goddess, the fruits of all accomplishments.",
 brief="The Devī asks for the easy remedy; Bhairava answers: the recitation itself.",
 logic="The hymn's frame: Bhairavī approaches Svacchanda Bhairava on Kailāśa and asks for the upāya for those who have broken the rules, however sincerely they try to atone. Bhairava's answer is not a ritual but a text — japādeva vimocanam, liberation by the recitation itself. It purifies the three channels, closes the chidras (the flaws and gaps in conduct and rite), and grants both bhoga and mokṣa. The logic of a remedy-hymn: the mantra is the medicine, and the disease is as much guilt as transgression.",
 howto="Recite it at the beginning and end of any ritual — the hymn's own instruction (yāgārambhe ca yāgānte). Also daily (nitya), on occasion (naimitika), when you want something (kāmya), for yourself or for someone else. Counting effects per the hymn: one hundred recitations purify even great sinners; fifty, inadvertent sins; twenty-five, minor sins — and a single recitation (of this hymn or of the Aghora japa) removes wrongs done by body, speech or mind, whether through inattention or knowingly. Feeling-tip: the ease is the point — sadupāyaṁ, the remedy without strain.",
 source_path="sources/bahurupa-meaning.pdf", source_ref="vv.5-7 · Academy recitation PDF"),
dict(id="bahurupa-close", section="sangha", title="No Mantra Greater",
 source="Śrī Bahurūpa-Garbha Stotra, the close (vv.13-15)",
 iast="vidhihīne pramāde ca japtavyaṁ sarva-karmasu | nātaḥ parataro mantro nātaḥ paratarā stutiḥ || nātaḥ paratarā kācit samyak-pratyaṅgirā priye | iyaṁ samaya-vidyānāṁ rāja-rājeśvarī-śvari || paramāpyāyanaṁ devi bhairavasya prakīrtitam | prīṇanaṁ sarva-devānāṁ sarva-saubhāgya-vardhanam ||",
 en="when the rule is missing, when there is negligence — it should be recited in every action. no mantra is greater than this, no praise higher; no counter-formula better than this, o beloved — this queen of the knowledge of the precepts, o sovereign among isvaras! this, o goddess, is the supreme nourishment of bhairava's glorification — it satisfies all the gods and increases all good fortune.",
 brief="The hymn's own claim: no mantra greater, no counter-formula better.",
 logic="Three closing claims: (1) it covers every action, including mistakes of omission and negligence (pramāda); (2) it is samyak-pratyaṅgirā — the perfect counter-charm against ritual flaw — the queen of samaya-vidyā, the knowledge of the precepts; (3) its effect is āpyāyana, nourishment — of Bhairava's glorification, pleasing to all the gods, increasing saubhāgya, all good fortune. The hymn then gives its own viniyoga: Ṛṣi Vāmadeva, meter Anuṣṭupa, devatā Bahurūpabhaṭṭāraka, purpose — removal of sins of body, speech and mind, and attainment of the four goals: dharma, artha, kāma, mokṣa.",
 howto="Full practice in the tradition: dhyāna of Svacchanda (crystal-white upward face, yellow east, blue south, pomegranate-red north, moon-white west — the twelve-verse meditation), then this hymn, then the Gāyatrī — oṁ bahurupāya vidmahe, koṭarākṣāya dhīmahi, tanno 'ghoraḥ pracodayāt, three times — then the mūla mantra. In this book's simpler use: one round of these three verses at the close of any difficult day; the line to remember is 'no mantra greater than this'.",
 source_path="sources/bahurupa-recitation.pdf", source_ref="vv.13-15 · viniyoga"),
]
CORPUS = json.load(open(HERE / "sources" / "shivastotravali_corpus.json"))


def deva(iast):
    if _tr is None:
        return ""
    try:
        out = _tr(iast, sanscript.IAST, sanscript.DEVANAGARI)
    except Exception:
        return ""
    return out.replace("\U0000A8F3", "\u0902").replace("\U0000A8F2", "\u0901")


def load():
    out = []
    for e in E:
        e = dict(e)
        if "corpus" in e:
            ch, v = e["corpus"]
            for c in CORPUS["chapters"]:
                if c["number"] == ch:
                    for vv in c["verses"]:
                        if vv["number"] == v:
                            e["iast"] = vv["iast"]
                            e["devanagari"] = vv["devanagari"]
        else:
            e["devanagari"] = deva(e["iast"])
        out.append(e)
    return out


def esc(s):
    return html.escape(s or "")


def dev_size(e):
    L = len(e["devanagari"])
    if L <= 90:
        return "40pt", "2.0"
    if L <= 150:
        return "32pt", "1.9"
    if L <= 240:
        return "25pt", "1.8"
    if L <= 340:
        return "20pt", "1.75"
    return "16pt", "1.7"


def en_size(e):
    L = sum(len(x) for x in e["en"].split("\n"))
    if L <= 140:
        return "15pt"
    if L <= 240:
        return "13.5pt"
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
.cover .om{font-family:'Tiro';font-size:60pt;line-height:1;margin-bottom:16mm;}
.cover h1{font-family:'Cormorant';font-weight:600;font-size:36pt;letter-spacing:.05em;margin:0;text-transform:uppercase;}
.cover .sub{font-size:15pt;font-style:italic;color:var(--grey);margin-top:4mm;}
.cover .rule{width:40mm;height:1px;background:var(--ink);margin:10mm auto;}
.cover .blurb{font-size:11pt;text-transform:uppercase;letter-spacing:.16em;color:var(--grey);}
.epi{display:flex;flex-direction:column;justify-content:center;text-align:center;}
.epi .skt{font-family:'Tiro';font-size:16pt;line-height:2;margin-bottom:6mm;}
.epi .en{font-style:italic;color:var(--grey);font-size:13pt;max-width:100mm;margin:0 auto;}
.epi .src{font-size:9.5pt;letter-spacing:.15em;text-transform:uppercase;color:var(--grey);margin-top:8mm;}
.toc h2,.sec-div h2,.bib h2{font-family:'Cormorant';font-weight:600;letter-spacing:.12em;text-transform:uppercase;font-size:13pt;color:var(--grey);}
.toc ol{list-style:none;padding:0;margin:6mm 0 0;column-count:2;column-gap:7mm;}
.toc li,.toc .sec{break-inside:avoid;-webkit-column-break-inside:avoid;}
.toc .sec{margin-top:4mm;font-size:9.5pt;letter-spacing:.18em;text-transform:uppercase;color:var(--grey);line-height:1.2;}
.toc li{margin:.4mm 0;font-size:11.5pt;line-height:1.3;}
.toc .n{color:var(--grey);display:inline-block;width:7mm;}
.sec-div{display:flex;flex-direction:column;justify-content:center;text-align:center;}
.sec-div .glyph{line-height:0;margin-bottom:5mm;}
.sec-div .num{font-family:'Cormorant';font-size:11pt;letter-spacing:.3em;color:var(--grey);}
.sec-div h2{font-size:26pt;letter-spacing:.06em;margin:4mm 0 0;color:var(--ink);text-transform:none;font-weight:600;}
.sec-div .sub{font-style:italic;color:var(--grey);font-size:13pt;margin-top:3mm;}
.sec-div .rule{width:30mm;height:1px;background:var(--ink);margin:8mm auto 0;}
.src{font-size:9.5pt;letter-spacing:.12em;text-transform:uppercase;color:var(--grey);}
.prayer{display:flex;flex-direction:column;}
.prayer h3{font-family:'Cormorant';font-weight:600;font-size:17pt;margin:2mm 0 0;text-align:center;}
.prayer .dev{font-family:'Tiro';text-align:center;white-space:pre-line;margin:8mm 0 0;}
.prayer .iast{font-style:italic;color:var(--grey);text-align:center;font-size:11pt;line-height:1.5;margin-top:4mm;}
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

    pages.append(f"""<section class="page epi"><div class="skt">{esc(deva(META['epi_iast']))}</div>
<div class="en">{esc(META['epi_en'])}</div>
<div class="src">{esc(META['epi_src'])}</div></section>""")

    pages.append("""<section class="page epi">
<div class="lines" style="text-align:left;max-width:none">
<span class="ln" style="font-size:14pt;font-weight:600;font-style:normal">Why these prayers</span>
<span class="ln" style="margin-top:6mm">Swami Lakshmanjoo compiled his Wisdom verses in the summer of 1987 and told his devotees: "These verses are for your daily recitation. Maybe sometime you will experience these stages."</span>
<span class="ln">Four of the six hymns in his recitation appendix live in these pages — the Krama Stotra, the Anuttarāṣṭikā, the Bhairava Stotra and the Dehastha — alongside the mealtime yajña he taught, the breath-japa of the Vijñāna Bhairava, and the dawn-dusk junction of the Tantrāloka: "the Lord must be worshipped at the point of the meeting of day and night."</span>
<span class="ln">Ten sections, one for each moment the day turns. Forty prayers, each facing its explanation — when to do it, how, why, and what it does. At the close: the two hymns chanted at his Weekly Sangha, the Aghora Mantra and the Śrī Bahurūpa-Garbha Stotra, with the notes from his own teaching.</span>
<span class="ln">Nothing here needs belief. The verses were built to be said — at the sink, at the desk, in the queue, in the dark.</span>
</div>
<div class="src">Practical Prayers</div></section>""")

    pages.append("""<section class="page epi">
<div class="lines" style="text-align:left;max-width:none">
<span class="ln" style="font-size:14pt;font-weight:600;font-style:normal">Reading a spread</span>
<span class="ln" style="margin-top:6mm">Each prayer sits beside its explanation. The left page is for the mouth — Devanagari big enough to fill the eye, the sound beneath it, the sense beneath that. The right page is for the mind: what the verse is actually doing, how to perform it, and what it is for.</span>
<span class="ln">Read the guide once when you meet the prayer. After that, only the prayer page matters — you'll know what lies behind it.</span>
<span class="ln">Take the one the day hands you: waking, bathing, social, work, food, waiting, negative, sick, positive, evening.</span>
<span class="ln">Every source is linked from its guide — the translations come from our Kashmir Shaiva corpus, the sangha hymns from the Lakshmanjoo Academy.</span>
</div>
<div class="src">Practical Prayers</div></section>""")

    toc = ['<section class="page toc"><h2>Contents</h2><ol>']
    for sid, num, title, sub in SECTIONS:
        toc.append(f'<div class="sec">{num} &nbsp; {esc(title)} <span style="opacity:.6">{esc(sub)}</span></div>')
        for e in [x for x in entries if x["section"] == sid]:
            toc.append(f'<li><span class="n">·</span>{esc(e["title"])}</li>')
    toc.append("</ol></section>")
    pages.append("".join(toc))

    n = 0
    for si, (sid, num, title, sub) in enumerate(SECTIONS, 1):
        pages.append(f"""<section class="page sec-div"><div class="glyph">{activity_glyph(sid, 18)}</div><div class="num">{esc(num)}</div>
<h2>{esc(title)}</h2><div class="sub">{esc(sub)}</div><div class="rule"></div></section>""")
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

    pages.append(f"""<section class="page epi"><div class="skt">ॐ शान्तिः शान्तिः शान्तिः</div>
<div class="en">peace, peace, peace</div>
<div class="src">Practical Prayers</div></section>""")

    pages.append("""<section class="page epi">
<div class="lines" style="text-align:left;max-width:none">
<span class="ln" style="font-size:14pt;font-weight:600;font-style:normal">The day, complete</span>
<span class="ln" style="margin-top:6mm">From the first light to the last breath, the day is one sequence of recognitions: you wake into his waking, wash a body that is his temple, walk out among his forms, work as his yoke, eat his offering, wait in his pace, meet your negatives as his play, rejoice in his victory, and hand the night back to his sleep.</span>
<span class="ln">The prayers are small; the day is the practice.</span>
</div>
<div class="src">Practical Prayers</div></section>""")

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
    bib.append("</ul></section>")
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
        print(f"  {num}. {title:<24} {len([x for x in entries if x['section']==sid])}")
    bad = [e["id"] for e in entries if not e.get("devanagari") or not e.get("iast")]
    print("incomplete:", bad or "none")
