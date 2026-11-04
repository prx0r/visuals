#!/usr/bin/env python3
"""Practical Prayers — 30 Trika prayers for the moments of the day.
Prayer page (type-filling Devanagari, Brahmārpaṇaṁ format) + facing explanation.
Run with the patala venv python (indic_transliteration)."""

import json, html, pathlib, re

HERE = pathlib.Path(__file__).parent
try:
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate as _tr
except Exception:
    _tr = None

META = dict(
    title="Practical Prayers",
    subtitle="Thirty Trika prayers for the moments of the day",
    blurb="food · waking · sleeping · waiting · negative · positive",
    epi_iast="brahmārpaṇaṁ brahma havir brahmāgnau brahmaṇā hutam",
    epi_en="the offering is brahman, the oblation is brahman, poured by brahman into the fire of brahman",
    epi_src="Bhagavad Gītā 4.24 — the meal prayer",
)

SECTIONS = [
    ("food", "I", "Food", "before eating"),
    ("wake", "II", "Waking", "on rising"),
    ("sleep", "III", "Sleeping", "at lights-out"),
    ("wait", "IV", "Waiting", "in the in-between"),
    ("negative", "V", "When You Are Negative", "fear · doubt · grief"),
    ("positive", "VI", "When You Are Positive", "rejoice · devote"),
]

# corpus refs: (chapter, verse) into shivastotravali_corpus.json
E = [
# ---------------- FOOD ----------------
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
dict(id="vbt-72", section="food", title="From Eating and Drinking",
 source="Vijñāna Bhairava v.72",
 iast="jagdhipānakṛtollāsarasānandavijṛmbhaṇāt | bhāvayed bharitāvasthāṃ mahānandas tato bhavet",
 en="from the swell of joy made by eating and drinking — from the blooming of bliss-rasa — one should imagine the full state; great bliss then may arise.",
 brief="Take the fullness of a meal and turn it into mahānanda.",
 logic="The dhāraṇā uses a given fact — eating already produces rasa and ullāsa, savour and lift — and makes that the object of bhāvanā: not the taste itself but the state of being filled (bharitāvasthā). Ordinary satiety is the raw material; great bliss the product, if attention stays on fullness instead of sliding to the next want.",
 howto="At the meal, not before. Eat to comfortable fullness, then pause with eyes half-open. Take one more spoonful of air, hold, and imagine the fullness radiating from the belly upward — chest, then head. Release. Three rounds. Don't chase ecstasy: the graded signal is that thinking quiets while the body stays warm. If drowsiness comes, stand up.",
 source_path="sources/vbt-p08.md", source_ref="v.72"),
dict(id="mpa-16", section="food", title="Food-Offering for the Ever-Content",
 source="Mahopadeśaviṃśatikā v.16",
 iast="nityatṛptasya naivedyaṃ tāmbūlaṃ ca kuto vibhoḥ | pradakṣiṇamanantasyā'dvitīyasyaya kuto natiḥ",
 en="food-offering for the ever-content, betel for the lord — whence? circumambulation for the endless, obeisance for the non-dual — whence?",
 brief="The litany asks: what can you offer to one who lacks nothing?",
 logic="The four closing rites of pūjā — naivedya (food offering), tāmbūla (betel), pradakṣiṇa (circumambulation), nati (obeisance) — all address a being who could lack something. Śiva lacks nothing. So the offering is not for him but for you: the act of offering is what turns eating into worship, not the food itself.",
 howto="Use it as the shrug before a meal: 'what can I offer the one who lacks nothing?' — then offer anyway. The humour is the doctrine. Feeling-tip: lightness, not solemnity. The verse makes the ritual joke that is also the deepest point.",
 source_path="sources/L2-mpa-p02.md", source_ref="v.16"),

# ---------------- WAKE ----------------
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
dict(id="svab-4", section="wake", title="Wake the Knowledge That Frees",
 source="Svabodhasiddhi v.4",
 iast="jayanty apārasaṃsārasārāsāravibhāgadāḥ | kaivalyajñānasaṃbodhahetavaś śambhavāṅghrayaḥ",
 en="victorious are śambhu's feet — they that tell the endless wheel of becoming from its essence and its refuse, and are the cause of the waking knowledge that frees.",
 brief="A dawn verse whose whole grammar is waking.",
 logic="Three functions stacked on the feet: they discriminate (saṃsāra's sāra against asāra — essence against refuse), they cause the knowledge that awakens (saṃbodhi-hetu), and they are victorious. Liberation is not granted but caused — through a knowledge that must wake, exactly like you.",
 howto="Say it once after the body-temple verse. Weight the word saṃbodha — waking. Picture a lamp being lit rather than a person bowing. Feel-test: does the line make the room sharper? Repeat at any hour when you have been awake but not waking.",
 source_path="sources/L2-svab-p01.md", source_ref="v.4"),
dict(id="param-35", section="wake", title="Waking, Dreaming, and the Fourth",
 source="Paramārthasāra v.35",
 iast="jāgrad viśvaṃ bhedāt svapnas tejaḥ prakāśamāhātmyāt | prājñaḥ suptāvasthā jñānaghanatvāt tataḥ paraṃ turyam",
 en="waking is the universe, through difference; dreaming is splendour, through the greatness of light; the knower is the state of sleep, through the massing of knowing; beyond that, the fourth.",
 brief="Abhinavagupta's census of the states — each credited with what it does best.",
 logic="Each state is honoured for its real contribution instead of being ranked: waking gives the many, dream gives light, sleep gives massed knowing. Only then is turya named — beyond the three, not as a fourth state but as what was never covered by them. The census dismantles the hierarchy.",
 howto="A morning inventory: touch each clause with a memory — this room, that dream, that blankness. Stop at tataḥ paraṃ turyam and don't try to produce a fourth; the verse says beyond, not within. Feeling-tip: after the third clause leave a half-beat of silence — that gap is closer to turya than any image.",
 source_path="sources/L2-param-p04.md", source_ref="v.35"),

# ---------------- SLEEP ----------------
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
dict(id="vbt-80", section="sleep", title="Gaze Down, Mind Unsupported",
 source="Vijñāna Bhairava v.80",
 iast="sthūlarūpasya bhāvasya stabdhāṃ dṛṣṭiṃ nipātya ca | acireṇa nirādhāraṃ manaḥ kṛtvā śivaṃ vrajet",
 en="of the gross-formed state — fixing the gaze downward, and swiftly: making the mind unsupported, one may go to śiva.",
 brief="The last practice before sleep: eyes down, mind unsupported, go.",
 logic="The bhāva is the gross — the day's residue, the body's weight; the gaze is set firm and lowered; the mind is made nirādhāra, without support: no image, no thought to rest on. Three conditions, one result — śivaṃ vrajet, one may go to Śiva. 'Go' is not travel; it is sleep without a holder.",
 howto="Lie down. Eyes half-open, lowered toward the pillow, then closed once the gaze has found its floor. Remove the mind's supports one by one: drop the plan for tomorrow, drop the commentary on the day, drop even the wish to sleep. What's left is a warm weight behind the sternum with no object — that is nirādhāra. If the mind grabs a support, note 'support' and set it down.",
 source_path="sources/vbt-p08.md", source_ref="v.80"),
dict(id="param-34", section="sleep", title="Creating, Keeping, Dissolving",
 source="Paramārthasāra v.34",
 iast="sṛṣṭisthitisaṃhārā jāgratsvapnau suṣuptam iti tasmin | bhānti turīye dhāmani tathāpi tair nāvṛtaṃ bhāti",
 en="creating, keeping, dissolving; waking, dreaming, deep sleep — these shine in him, in the fourth abode; and unveiled he shines, not covered by them.",
 brief="The states are lights in a room; the room is not covered by them.",
 logic="The macro (creation, maintenance, dissolution) is mapped onto the micro (the three states), both placed in turīya, the fourth abode. The load-bearing clause: tathāpi tair nāvṛtam — yet not veiled by them. Turīya is not a fourth experience but what remains unveiled while the others shine.",
 howto="A sleep primer, slowly: the three acts — pause — the three states — pause — then hold nāvṛtam (unveiled) as the last word you hear. The feeling: a screen behind the mind's pictures that stays clear while pictures change. Don't try to enter turya; the verse points at what is not covered. Sleep then arrives without touching the unveiled.",
 source_path="sources/L2-param-p04.md", source_ref="v.34"),
dict(id="sst-9-14", section="sleep", title="At Your Cool Feet", corpus=[9,14],
 source="Utpaladeva, Śivastotrāvalī 9.14",
 en="when will i lie down — free of every object, settled in the embrace of undiminished glory — at your two cool lotus feet?",
 brief="The sleep prayer: the cool feet are the peace after the fever of wanting.",
 logic="Utpaladeva asks when he will lie down free of every object (aśeṣaviṣaya — no grasping left), settled in undiminished glory (aśūnya śrī), at the two cool lotus feet (śītāṅghri-kuśeśaya). 'Free of every object' is not blankness but the rest that remains when the mind stops reaching. The cool feet are the peace of Śiva.",
 howto="In bed. Say it once, then let the image of the two cool feet form under the mind's eye — no details needed, just the coolness. The feeling to find: the fever of the day dropping. If the mind races, return to the coolness, not the words.",
 source_path="sources/sivastotravali_corpus.json", source_ref="9.14"),

# ---------------- WAIT ----------------
dict(id="sst-16-8", section="wait", title="I Don't Mind", corpus=[16,8],
 source="Utpaladeva, Śivastotrāvalī 16.8",
 en="in crisis or at ease, weeping or laughing, grave or unhinged — by devotion, lord, let me be so.",
 brief="The api-chain refuses resolution: everything is allowed.",
 logic="The verse piles up opposites with 'api' (even): viṣama/sthāna (crisis/peace), rudann/hasann (weeping/laughing), gambhīro/vicitta (grave/unhinged). Devotion is not the absence of any of them; it is what holds them. The prayer does not ask for calm — it asks to be devotion through whatever arrives.",
 howto="Use it when waiting has turned into agitation — a queue, a delay, a message that won't come. Say it once inwardly. Don't wait for composure: the very mess is the place where devotion can be. Feeling-tip: the shoulders drop half a millimetre; that's the api doing its work.",
 source_path="sources/sivastotravali_corpus.json", source_ref="16.8"),
dict(id="sst-1-1", section="wait", title="Methodless Devotion", corpus=[1,1],
 source="Utpaladeva, Śivastotrāvalī 1.1",
 en="i bow to that devotee who is glorified with the devotion of lord śiva and to whom the appearance of lord śiva takes place without conducting meditation or recitation of any kind.",
 brief="No method needed — the waiting itself is the devotion.",
 logic="The opening verse of the Śivastotrāvalī: the devotee to whom Śiva appears without dhyāna or japa (avidhipūrvakam — methodless). The bow is to a state where nothing is being done. Waiting is exactly that state: nothing to do, nowhere to go, and yet not nothing.",
 howto="In a queue, on a train, waiting for news: say 'I bow to that devotee' and recognise yourself as the one described. No technique. The waiting is already the practice. Feeling-tip: the hands can rest; the attention does not need to grasp.",
 source_path="sources/sivastotravali_corpus.json", source_ref="1.1"),
dict(id="sst-17-19", section="wait", title="In Every Action", corpus=[17,19],
 source="Utpaladeva, Śivastotrāvalī 17.19",
 en="o lord, may i experience, moment by moment, in every action, the great joy of drinking the nectar of your worship.",
 brief="The in-between moment becomes the practice itself.",
 logic="Utpaladeva prays for the taste of worship inside every action — not more ritual, but the nectar of pūjā in the ordinary. 'Moment by moment' (kṣaṇāt kṣaṇam) is the whole method: the repeated return of attention. Waiting is full of kṣaṇas — this verse makes them the site of the drink.",
 howto="At any transition or pause: say it once, then take one breath as if that breath were the nectar. Don't manufacture joy — notice the small lift that a pause already gives. Three pauses, three sips, and the waiting has changed colour.",
 source_path="sources/sivastotravali_corpus.json", source_ref="17.19"),
dict(id="anu-1", section="wait", title="No Method", source="Abhinavagupta, Anuttarāṣṭikā v.1",
 iast="saṃkrāmo 'tra na bhāvanā na ca kathāyuktir na carcā na ca dhyānaṃ vā na ca dhāraṇā na ca japābhyāsaprayāso na ca | tat kiṃ nāma suniścitaṃ vada paraṃ satyaṃ ca tacchrūyatāṃ na tyāgī na parigrahī bhaja sukhaṃ sarvaṃ yathāvasthitaḥ",
 en="there is no crossing over here — no contemplation, no discussion, no visualization, no steadying, no effort of japa. so what is decided? speak the supreme truth: not a renouncer, not a possessor — enjoy happiness, all of it, staying exactly as you are.",
 brief="The anupāya: when every method is denied, waiting is the answer.",
 logic="The verse takes away every method — bhāvanā, kathā, carcā, dhyāna, dhāraṇā, japa — and leaves one instruction: stay as you are (yathāvasthitaḥ), enjoy happiness, neither renouncing nor grasping. Waiting is yathāvasthitaḥ in its purest form: nothing to do, nothing to fix.",
 howto="When waiting becomes restless, say the verse — or just its last line, 'stay exactly as you are.' The trying to become something is the only distance. Feeling-tip: the restlessness is allowed to sit; you don't argue with it; you just stay.",
 source_path="sources/anuttarastika.md", source_ref="v.1"),
dict(id="sst-12-25", section="wait", title="Don't Control the Swift Mind", corpus=[12,25],
 source="Utpaladeva, Śivastotrāvalī 12.25",
 en="i don't want to control my mind because the mind is so swift, you cannot catch it.",
 brief="Let the mind roam in the waiting; skill within, not restraint.",
 logic="Lakshmanjoo's gloss: the mind is too swift to catch, so the verse does not ask for control. The practice is skill within roaming (svarasena pracaraty api) — not catching the mind but being with it as it moves. Waiting is when the mind roams most; this verse blesses the roaming.",
 howto="In the waiting, watch the mind go where it goes — plans, memories, fantasies — without steering. The skill is staying with it, not against it. Feeling-tip: a slight amusement at how fast it moves; that amusement is already the 'worship-skilled' state the verse asks for.",
 source_path="sources/sivastotravali_corpus.json", source_ref="12.25"),

# ---------------- NEGATIVE ----------------
dict(id="bh-5", section="negative", title="I Never Fear", source="Abhinavagupta, Bhairavastava 5",
 iast="ittham upoḍhabhavanmayasaṃviddīdhitidāritabhūritamisraḥ | mṛtyuyamāntakakarmapiśācair nātha namo'stu na jātu bibhemi",
 en="thus, with the great darkness torn open by the rays of the consciousness become you — lord, namas; i never fear, not from death, from yama, from the ender, from the ghosts of karma.",
 brief="Fearlessness as salutation, not as courage.",
 logic="Awareness has already torn the darkness; what remains is not courage but salutation. The devotee still names death's ministers — Mṛtyu, Yama, the ender, the karma-ghosts — and bows to them, because they too are Śiva's play. 'I never fear' is the natural temperature of recognition.",
 howto="Recite when fear arrives — not to banish it but to salute it. The fear is named, bowed to, and left standing. Feeling-tip: the chest opens rather than tightens; the bow is physical as well as verbal. Do it at night, or in the moment before the difficult thing.",
 source_path="sources/bhairavastava.md", source_ref="bh-p05"),
dict(id="bh-3", section="negative", title="No Fear-Talk", source="Abhinavagupta, Bhairavastava 3",
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
dict(id="sst-2-8", section="negative", title="Saṃsāra and Beyond", corpus=[2,8],
 source="Utpaladeva, Śivastotrāvalī 2.8",
 en="to the one who is the sole cause of saṃsāra and the sole opponent of saṃsāra; to śambhu, who is the form of saṃsāra and is beyond saṃsāra, namas.",
 brief="No enemy outside: bondage and release are the same Lord.",
 logic="A paradox of the recognition: the one who causes saṃsāra also destroys it; Śambhu is its form and also beyond it. There is no enemy to defeat outside the self. When you feel negative about the world, this verse says: the world's very form is Śambhu.",
 howto="When the world feels like the problem, say it. The split between 'spiritual' and 'worldly' is the only saṃsāra. Feeling-tip: the irritation with the world softens into recognition; the same world, seen as his form, is no longer an attack.",
 source_path="sources/sivastotravali_corpus.json", source_ref="2.8"),
dict(id="svab-6", section="negative", title="The Knife That Cuts the Knot",
 source="Svabodhasiddhi v.6",
 iast="mamāham iti hṛdgranthicchedanaikakṛpāṇikām | spandāspandakṛtagrāsāṃ naumy ahaṃ śuddhasaṃvidam",
 en="i bow — i — to pure awareness: the knife that alone cuts the heart's knot of 'mine' and 'i', the one that has swallowed both the throb and its stillness.",
 brief="For guilt and possessiveness: one cut, and the knot is gone.",
 logic="The knot (granthi) is mamāham — 'mine' and 'I', two threads. The instrument is a kṛpāṇa, a knife, and only one does it: pure awareness. And the knower's own domain — throb and stillness — has already been swallowed by that knife. 'I bow — I' stages the surrender: the pronoun survives long enough to bow, then is cut too.",
 howto="Recite with a hand flat over the sternum. Weight the first aham: feel where your 'I' sits in the body, and on 'naumy ahaṃ' press gently and let that place soften. The image is a blade, but the feeling is a release of grip, not a strike — knots untie. Fastest on small knots (a slighted email), slower on old ones.",
 source_path="sources/L2-svab-p01.md", source_ref="v.6"),

# ---------------- POSITIVE ----------------
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
dict(id="sst-20-8", section="positive", title="The Stone Pillar Worships", corpus=[20,8],
 source="Utpaladeva, Śivastotrāvalī 20.8",
 en="o lord śiva, when a devotee of thee has created this itching sensation of bhakti (devotion), and that itching won't be removed until you are there, you are present. your main presence will remove that itching sensation.",
 brief="When devotion itches, even a stone pillar becomes worship.",
 logic="The verse takes the itch of bhakti (bhaktikaṇḍū) — the restless longing — and says that when it arises, even a mahānikaṣapāṣāṇasthūṇa, a great stone pillar, becomes pūjā, worship. The longing itself is the worship; you don't need the right posture or place.",
 howto="When the positive urge to connect arrives — the itch — don't damp it. Say this and let the itch be the offering. The feeling: a restless sweetness that doesn't need a destination. Even waiting with the itch is already the pillar being worshipped.",
 source_path="sources/sivastotravali_corpus.json", source_ref="20.8"),
dict(id="spandasandoha-1", section="positive", title="He Alone Wins",
 source="Kṣemarāja, Spandasandoha 1",
 iast="sa jayati śiva ekaḥ spandavān svapratiṣṭhaḥ yo'ntarvaktraṃ rasayati",
 en="he alone wins — śiva, possessor of the pulse, self-established, who makes the inner face taste.",
 brief="A one-line victory song for the moment everything is right.",
 logic="Kṣemarāja's condensation of the Spandakārikā: Śiva alone wins — he who possesses the pulse (spanda), is self-established, and makes the inner face taste. 'The inner face' is attention turned back on itself; to taste it is the whole of the practice. The verse is already in the register of victory.",
 howto="Say it when the recognition lands — when you see, when you taste, when the pulse is obvious. It's a salute, not a request. Feeling-tip: the slight pride in 'he alone wins' is allowed; it's his victory you're naming, and yours for seeing it.",
 source_path="sources/spandasandoha.md", source_ref="v.1"),
dict(id="spanda-1", section="positive", title="The Wheel of Powers",
 source="Vasugupta, Spandakārikā 1.1",
 iast="yasyonmeṣanimeṣābhyāṃ jagataḥ pralayodayau | taṃ śakticakravibhavaprabhavaṃ śaṅkaraṃ stumaḥ",
 en="to him by whose opening and closing the world dissolves and arises — to śaṅkara, source of the glory of the wheel of powers, we sing.",
 brief="The opening hymn: the world blinks, and we sing to the one who blinks it.",
 logic="The Spandakārikā opens with a hymn to the pulse: by the Lord's opening and closing (onmeṣa-nimeṣa — his blink) the world dissolves and arises. The 'wheel of powers' is the circle of śaktis through which consciousness manifests. To sing is to join the pulse rather than resist it.",
 howto="Recite when the world feels vivid — when colours are sharp, when music lands, when the pulse is obvious. It's a song of participation. Feeling-tip: blink with the verse; the world dissolving and arising on each blink is literal enough.",
 source_path="sources/spanda.md", source_ref="Spandakārikā 1.1"),
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
.cover .om{font-family:'Tiro';font-size:64pt;line-height:1;margin-bottom:16mm;}
.cover h1{font-family:'Cormorant';font-weight:600;font-size:36pt;letter-spacing:.05em;margin:0;text-transform:uppercase;}
.cover .sub{font-size:15pt;font-style:italic;color:var(--grey);margin-top:4mm;}
.cover .rule{width:40mm;height:1px;background:var(--ink);margin:10mm auto;}
.cover .blurb{font-size:11pt;text-transform:uppercase;letter-spacing:.16em;color:var(--grey);}
.epi{display:flex;flex-direction:column;justify-content:center;text-align:center;}
.epi .skt{font-family:'Tiro';font-size:16pt;line-height:2;margin-bottom:6mm;}
.epi .en{font-style:italic;color:var(--grey);font-size:13pt;max-width:100mm;margin:0 auto;}
.epi .src{font-size:9.5pt;letter-spacing:.15em;text-transform:uppercase;color:var(--grey);margin-top:8mm;}
.toc h2,.sec-div h2,.bib h2{font-family:'Cormorant';font-weight:600;letter-spacing:.12em;text-transform:uppercase;font-size:13pt;color:var(--grey);}
.toc ol{list-style:none;padding:0;margin:6mm 0 0;}
.toc .sec{margin-top:4mm;font-size:9.5pt;letter-spacing:.18em;text-transform:uppercase;color:var(--grey);line-height:1.2;}
.toc li{margin:.4mm 0;font-size:11.5pt;line-height:1.3;}
.toc .n{color:var(--grey);display:inline-block;width:7mm;}
.sec-div{display:flex;flex-direction:column;justify-content:center;text-align:center;}
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

    toc = ['<section class="page toc"><h2>Contents</h2><ol>']
    for sid, num, title, sub in SECTIONS:
        toc.append(f'<div class="sec">{num} &nbsp; {esc(title)} <span style="opacity:.6">{esc(sub)}</span></div>')
        for e in [x for x in entries if x["section"] == sid]:
            toc.append(f'<li><span class="n">·</span>{esc(e["title"])}</li>')
    toc.append("</ol></section>")
    pages.append("".join(toc))

    n = 0
    for sid, num, title, sub in SECTIONS:
        pages.append(f"""<section class="page sec-div"><div class="num">{esc(num)}</div>
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
