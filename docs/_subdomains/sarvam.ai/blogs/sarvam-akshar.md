---
url: https://sarvam.ai/blogs/sarvam-akshar/
title: Introducing Sarvam Akshar | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:17:21.645612+00:00
---

# Introducing Sarvam Akshar | Sarvam AI

> Source: https://sarvam.ai/blogs/sarvam-akshar/

  1. [ Home ](https://sarvam.ai/)
  2. /
  3. [ Blog ](https://sarvam.ai/blogs)



# Introducing Sarvam Akshar

A document intelligence workbench built on Sarvam Vision, enabling grounded reasoning, layout-aware extraction, and automated proofreading.

Product

[Try Akshar](https://akshar.sarvam.ai/)

* * *

Feb 15, 2026·5 min readShare

![Introducing Sarvam Akshar](https://assets.sarvam.ai/tr:w-1600,q-90,f-auto,dpr-auto/images/03117ysv/production/fff4fe106a03242dec49bd27025e1b55a51de0b9-1800x1350.png)

We recently released Sarvam Vision - a state-of-the-art 3B vision-language model for document intelligence in English and 22 Indian languages. The model achieves best-in-class scores on global benchmarks like olmOCR-Bench and OmniDocBench for English; and obtains leading accuracy on the Sarvam Indic OCR Bench for Indian languages better than frontier models such as Gemini 3 Pro, Opus 4.5, and GPT-5.2.

Today we release Akshar - a workbench tailored to solve last-mile problems in knowledge extraction. Akshar functions as the intelligence layer atop the Sarvam Vision model moving beyond passive text extraction to active reasoning. The platform equips agents with critical information - visual grounding, semantic layout details, block-level extractions - to enable automated proofreading and error corrections.

### The Limits of Existing Solutions for Document Digitization

##### Legacy OCR Stack

Classical OCR engines - ranging from open-source staples like Tesseract and EasyOCR to enterprise APIs like Google Cloud Vision - face significant architectural constraints when processing complex, unstructured documents. These systems typically rely on a bottom-up approach, identifying characters and words in isolation without understanding the semantic or spatial context of the page. This limitation manifests as a failure in layout analysis, where multi-column contents are read linearly across the page, resulting in discontinuous text.

Furthermore, these models struggle profoundly with Indic scripts, frequently misinterpreting complex conjuncts and diacritics (matras), or failing to distinguish between body text and marginalia. Such lack of semantic understanding and context of a page renders the output unusable for downstream use cases which require full accuracy.

##### Multimodal Large Language Models

While modern VLMs have made major strides in document understanding, they are no silver bullet. Frontier models continue to yield low-accuracy outputs as complexity of a document increases (e.g., historical newspapers in Indian languages, publications with embedded charts, among others). This class of models have solved problems such as reading order prediction, key-value extraction, and multimodal understanding. However, they introduced additional gaps - such as probabilistic outputs, lack of auditability, and required manual tuning of prompts leading to factual inconsistencies.

##### What remains unsolved?

Despite all recent progress, several last-mile complexities persist: (a) zero-shot parsing of complex layouts without training; (b) capturing semantic relationships between elements; (c) visual grounding; (d) automated error localization and correction with human-in-the-loop at scale.

### Sarvam Vision x Akshar: A Knowledge Extraction Workbench

Built upon Sarvam Vision’s capabilities, Akshar takes a more fundamental approach to document processing. Let’s take the case of digitizing historical documents dating back to the 1800s. The 19th-century Gujarati or Tamil manuscripts, archaic fonts and complex conjuncts (matras) often are hallucinated modern spellings at baseline. A raw API output requires a linguist to compare the text against the image line-by-line - a prohibitively slow process. Akshar solves this by coupling the VLM with an agents loop. The workbench can identify script uncertainties allowing experts to validate hundreds of pages in the time it typically takes to transcribe one.

##### Visual grounding

Pinpoint exact coordinates of text and elements in documents.

### Source document

Input

![English newspaper: source document with bounding boxes](https://assets.sarvam.ai/tr:q-70,f-auto,dpr-auto/assets/products/doc-agents/samples/english-news.webp)

Click a block to scroll to its text

### Akshar

Sarvam

Extracted blocks · 94 detected

1\. Header

AMRITA BAZAR PATRIKA INDEPENDENCE NUMBER

2\. Header

August 15, 1947.

3\. Headline

HIGH PRIEST OF REVOLUTION Sri Aurobindo's Role In Freedom Movement

4\. Image

The image provided is a low-resolution, grayscale portrait photograph of a man. It is not a chart, graph, or technical diagram containing data. The subject is facing forward, though the image quality is grainy, making specific facial features difficult to discern. He appears to be wearing a light-colored, patterned garment, possibly a checkered shirt or sweater. As this is a photograph of a person and not a data visualization, there are no axes, legends, or numerical data points to extract.

5\. Footnote

Sri Aurobindo as leader of Swadeshi movement

6\. Paragraph

THE first rays of the dawn of free- dom in India are visible in her skies. The children of this hoary land are breathing airsh the ex- hilarating air of that free life of which they were deprived for cen- turies. The struggle of India for her political independence has ended in a glorious victory. But the task ahead of building up a new India is a tremendous one, requiring as it does, the applica- tion of the utmost capacities of the race. The endeavour, therefore, must never cease, the endeavour to recon- struct the national life on the basis of India's own culture, the truth of her soul and the purpose of her existence. Indeed the free India of to-day is not at all what she is destined to be. Her territorial integrity, her political one- ness is of vital importance to her un- hampered growth as a nation so as to be the leader of all mankind. Verily it is that for which she has lived through the ages. A resurgent India, a strong, united and illuminated India is the hope and need of humanity to-day. And when she becomes that, who reaches the noontide of her freedom and greatness.

7\. Paragraph

the birth of men who as well as the movements that go in their names, were at once the pioneer and precursors of a glorious future for the country. They made the pioneer attempts to win back for India whatever she had lost during her long period of decline. But very lit- tle of a definite nature was then done towards the political uplift of the peo- ple. It was about the close of the last century and the beginning of the pre- sent that a few rare sons of India felt within them the pangs of her subje- tion and strove for the attainment of her freedom so that she might fulfili herself both as a nation and as a savi- our of mankind. But the movement was not a mere political one. There was a deeper side to it which must be under- stood if a proper appraisal is to be made of that movement, and without which the essential intention, the true truth of India's struggle for freedom, will re- main an undiscovered secret.

8\. Paragraph

# RISE OF THE INDIVIDUAL Of the two forces that in the last century proved most effective in the individual and collective life of Europe, one was the French Revolution and the other was the scientific materialism. It was an age when the marvellous achievements of Science made the in- dividual conscious of his powers and potentialities and when the great ideals of revolutionary France roused the col- lectivity to a sense of its rights and re- sponsibilities. Those influences, however, were not confined to Europe only. The mind of Asia, though naturally inclined to conservatism did not take long to imbibe them. In India their impact produced results that helped to prepare the ground for an awakening in her national life. The inward bent of their mind opened the inaugurators of this awakening not only to the puissance and capacity of India's intellect and heart but also to her inherent spiritual genius and the magnificent treasures of her past.

9\. Paragraph

It was this latter fact-the redis- covery of the eternal truths seen by the ancient fathers-that made Viveka- nanda declare that India has a work to do for the spiritual liberation of man and that she must, therefore, rise and conquer the world by the power of her soul.

10\. Paragraph

The Swamp's was indeed a voice that spoke in the accents of the Gods. It stirred the country to its inmost depths and gave a rude shak- ing to the Leviathan that had been sleeping so long.

11\. Section Title

THE LEVIATHAN WAKES

12\. Paragraph

The Leviathan woke up, and signs of a new resurgence began to be percep- table in every sphere of the nation's life. As their knowledge of the past in- creased and deepened, the children of the Mother felt inspired from within to reinstall her in her rightful place in the world as the Oraculous Mother of man whom she would emancipate from darkness and discord and suffering by the light of her acosian wisdom. But the fact was also clear that India could not fulfill this aim so long as she was in bondage. She must, therefore, be free, free in every sense of the term, that is to say, India will be free in India as an Englishman is free in Eng- land. This is the inner meaning of In- dia's struggle for her political independ- ence.

13\. Paragraph

It was Bankim Chandra Chatterjee who first saw the vision of Mother India, the Mother as she was in her glorious past, as she is in her hap- less present, as she will be in her even more glorious future, and in an inspired moment uttered the mantra of awakened nationalism. 'Bande Mataram' soon became the mantra of power by which the Mother was invoked, and the Mother poured her shakti into her children and fired them with a burning desire to dedicate themselves to the cause of their country's freedom.

14\. Paragraph

Sri Aurobindo called Bankim a Rishi, a seer, and revealed to the country the truth of the 'mantra'. He wrote: "The mantra had been given and in a single day a whole people had been converted to the religion of patriotism. The Mo- ther had revealed herself. Once that vision has come to a people, there can be no rest, no peace, no further sham- ber till the temple has been made ready, the image installed and the sacrifice offered. A great nation which has had that vision can never again bend its neck in subjection to the yoke of a con- queror." If Bankim was the seer of the national mantra, Sri Aurobindo was the God-appointed high-priest and prophet of national freedom who delivered the gospel of dynamic nationalism and chalked out the main lines of action for its growth and fulfillment.

15\. Paragraph

But was Sri Aurobindo only an evan- gelist a revolutionary or mere leader of a political movement? And was liberation of India the sole objective of all his activities in those days? The life of Sri Aurobindo, as he has him- self said, has never been on the sur- face for man to see. Next to nothing was known about him even when he was most active in working out the revolu- tionary programme. He preferred to re- main and act and even to lead from behind the scenes without his name being known to the public. It was the Government's action to preventing him as the editor of the Bande Mataram that forced him into the public view. Not yet in his teens, while so Man- chester, he used often to use vicious of

16\. Paragraph

"Is it a mere coincidence that Sri Aurobindo's birthday, the 15th August, synchronises with the day of India's free- dom? It is a day of that supreme victory for India, which will crown her with the leadership of mankind. A new age of the Spirit is in sight and it must begin with a spiritual awakening, of which this holy land will be the first centre."

17\. Paragraph

It is therefore profitable to go through the unique care- er of the "Poet of Patriotism, the Prophet of Nationalism and the Lover of Humanity" (the epithets used by C. R. Das at Sri Aurobindo's trial in 1908) and remember that it was Sri Aurobindo who was behind the first revolutionary movement. It was he who first gave the ideal of complete independence and said 'first freedom, then regeneration,' 'Nationalism is immortal,' and spoke of the need of resur- gence of Asia as early as 1909-the fulfilment of which we see to-day.

18\. Paragraph

In this splendid article, St. Mitra, who was for years associated with Tagore in the Viswabharati and now lives in Pondicherry Asram, makes a survey of Sri Aurobindo's life and reminds us that Sri Aurobindo's ideal as regards free- dom of India has been realised. Sri Aurobindo knew long back that it would be so, and went deeply into Sadhana from 1910 to get ready for India's God-given mission, to- wards the fulfilment of which turdependence is the first step.

19\. Headline

(By Slair Kumar Mitra)

20\. Paragraph

a new world that would be born and of an 'age of gold' that would dawn on earth. In 1907 he wrote: "I have in me the power to accomplish the deliverance of my fallen country, but it is not any physical power. It is the power of know- ledge,-'Brashimatz' founded in 'Jnana'. God has sent me to this world to do this work, the seed of which first germi- nated when I was fourteen years of age and it took a deep root in me when I was eighteen." About the same time he wrote again: "I have come to do God's work." These are thoughts that show the uniqueness of his personality. And his later life is a glowing illustra- tion of it.

21\. Paragraph

It was in the nineties of the last cen- tury, a few years after his arrival at Baroda, that Sri Aurobindo began to give some form to his revolutionary ideas that must have been growing in him from his early days. Freedom of his country seemed to him then to be the first consideration, and he be- lieved that only by a revolution could it be brought about. Inspite of odds almost formidable in nature, he dared to think in those days that a move- ment of liberation through violent re- sistance and revolt becoming more and more general and persistent would com- pel the British people to accommodate Indian aspiration so as to save what they could of their empire or, in an extremity, decide to grant independence rather than have it forcibly wres- ted from their hands.

22\. Paragraph

Sri Aurobindo made his first move when he sent a young Bengali sol- dier of the Baroda army, Jatin Baserji, as his lieutenant to Bengal with a programme of preparation and action which he thought might occupy thirty years before fruition could become possible. As a matter of fact it has taken 50 years for the movement of freedom to arrive at the beginning of fruition and suc- cess.

23\. Section Title

THE DECISIVE MOVE

24\. Paragraph

The idea was to establish secretly, or so far as visible action could be taken under various pretexts and covers, re- volutionary propaganda and recruiting throughout Bengal. This was to be done among the youth of the country while sympathy and support and financial and other assistance were to be obtained from older men who had advanced views or could be won over to them. Centres were to be established in every town and eventually in every village, societies of young men were to be es- tablished with various ostensible ob- jects, cultural, intellectual or moral and those already existing were to be won over for revolutionary use. Young men were to be trained in activities which might be helpful for ultimate military action, such as riding physical training, athletics of various kinds, drill and organised movement.

25\. Paragraph

As soon as the idea was sown it at- tained a rapid progress; already small existing groups and associations of young men who had not yet the clear idea or any settled programme of revo- lution began to turn in this direction and a few who had already the revo- lutionary aim were contacted and soon developed activity on organised lines; the few rapidity became the many.

26\. Section Title

THE IDEA CATCHES

27\. Paragraph

Sri Aurobindo's aim was to bring about a close organisation of the whole movement, but it did not entirely mate- rialised. Nevertheless, the movement lit- self did not suffer by that, for the general idea was taken up and the ac- tivity of many separate groups led to greater and more widespread diffusion of the revolutionary idea and its acti- villes. Afterwards there came the Par- tition of Bengal and a general outburst of revolt which was so readily possible because of Sri Aurobindo's preparation of the ground for it, and which now fa- voured the rise of the Extremist Party and the great Nationalist movement.

28\. Paragraph

Sri Aurobindo's activities were then turned more and more in this direction and the secret action became a second- ary and subordinate element. He took advantage, however, of the Swadeshi movement to popularise the idea of vio- lent revolt in the future. The Bengal daily paper 'Yugantar' began under his guidance to preach open revolt and the absolute denial of British rule and in- cluded such items as a series of articles containing instructions for guerilla warfare. Sri Aurobindo himself wrote in Bengali some of the opening articles in the early numbers of the paper. The paper at once acquired an immense in- fluence over the minds of all young men in the Province.

29\. Paragraph

It may be noted that the Secret Society did not include terrorism in its programme, but this element grow up in Bengal as a result of the strong repression and the reaction to it in the province.

30\. Paragraph

BIRTH OF NATIONALIST PARTY Conditions were now favourable to the formation of the Nationalist Party, of which Sri Aurobindo was a prominent leader. He was also its principal leader in action in Bengal and the organiser of its policy and strategy. He had de- cided in his mind the lines on which he wanted the country's action to run: what he planned was very much the same as was developed afterwards in Ireland as the Sinn Fein movement, but Sri Aurobindo did not derive his ideas, as some have represented, from Ire- land, for the Irish movement became prominent later and he knew nothing of it till after he had withdrawn to Pondicherry.

31\. Paragraph

Sri Aurobindo had now to establish and generalise the idea of independence in the mind of the Indian people and at the same time to push first a party and then the whole nation into an in- tense and organised political activity which would lead to the accomplish- ment of that ideal.

32\. Paragraph

His idea was to capture the Con- gress and make it an instrument of revolutionary action instead of a centre of a timid constitutional agi- tation which could talk and pass resolutions and recommendations to the foreign government; if the Con- gress would not be captured then a central revolutionary body would have to be created which could do this work, It was to be a sort of state within a State giving its directions

33\. Paragraph

to the people and creating organised bodies and institutions which would be its means of action; there must be an increasing non-cooperation and passive resistance which would ren- der the administration of the coun- try by a foreign government diff- cult or finally impossible, a univer- sal unrest which would wear down repression and finally, if need be, an open revolt all over the country.

34\. Section Title

THE PROCLAMINE

35\. Paragraph

This plan included a boycott of Bri- tish trade, the substitution of national schools for the Government institutions, the creation of arbitration courts to which the people could resort instead of depending on the ordinary courts of law, the creation of volunteer forces which would be the nucleus of an army of open revolt and all other action that would make the programme complete. The idea of boycott took firm roots in

36\. Image

The provided image is a low-resolution, grayscale portrait photograph of a person. It appears to be a historical photograph, possibly from a newspaper or archival document, given the grainy texture and monochromatic quality. The subject is a woman facing forward with a neutral expression. She has short hair styled with a distinct, thick braid or headwrap wrapped around the top of her head. She is wearing a dark, high-collared garment. The background is dark and indistinct. As this is a photograph of a person and not a chart, graph, or technical diagram, there are no axes, legends, numerical data, or trends to analyze.

37\. Footnote

Bankim Chandra Chatterjee, who gave "Bande Mataram" mantram

38\. Paragraph

the country, that of national education materialised in the starting of many national schools in various parts of the country. Some districts took up the idea of people's court not without success. The volunteer groupings however had a saronger vitality. They lived on in many shapes and multiplied in formations. These workers were the spearhead of the movements of direct action which broke out from time to time in the struggle for freedom.

39\. Paragraph

But the greatest thing done in those years was the creation of new spirit in the country. In the enthusiasm that swept surging everywhere with the cry of "Hande Mataram" ringing on all sides men felt it glorious to be alive and dare and act together and hope; the old apathy and timidity was broken and a force created which nothing could destroy and which rose again and again in wave after wave till it has carried India to the beginning of a complete victory.

40\. Paragraph

The part Sri Aurobindo took publi- city in indian politics was of brief dura- tion, for he turned aside from it in 1910 and withdrew to Pondicherry, much of his programme lapsed in his absence, but enough had been done to change the whole face of Indian politics and the whole spirit of the Indian people, to make independence its aim and non- co-operation its method, and even its imperfect application heightening into apocalyptic periods of revolt has been sufficient to bring about its victory. The course of subsequent events followed largely Sri Aurobindo's ideas. The Congress was finally captured by the Nationalist Party, declared independence its aim, organized itself for action, took almost the whole nation minus a major- ity of the Mohammedans and a mono- rity of the Depressed classes into ac- ceptance of its leadership and eventu- ally formed the first National indepen- dent Government in India.

41\. Paragraph

Sri Aurobindo had no long been a silent leader. His ideas were within him, known only to his co-workers and followers and by the form they were given under his guidance. His only political writings dur- ing the nineteen of the last century were the articles in the 'Induprakasha' of Bombay, in which he severely criticized the Medi- rate politics denouncing it as mere men- diness. But they were published anonymously. His association with the 'Bande Mataram'-that fiery organ of dynamic na- tionalism-gave him an opportunity to pro- pagate his inspiring thoughts and wonder- ful visions.

42\. Paragraph

The paper first declared its policy to be "complete autonomy, free from Bri- tish control," but Mr Ameryhindo soon knew aside too cautious and complex phrase for the single word 'independent', which he was the best to declare publicly as the one goal of the Indian political movement. This was towards the end of 1906. A few months later he wrote:

43\. Section Title

DIVINE POWER SEEN

44\. Paragraph

A Divine Power is behind the movement, the Self-Ocean, the Time-Spirit, is at work to being about a mighty movement of which: the world at the present juncture has need. That movement is the resurgence of Asia and the resurgence of India is only a neces- sary part of the larger movement but its central need, India is the key-stone of the arch, the chief authenticity of the common Asian destiny......The idea of a free and united India has been born and arrived at full stature in the land of the Muslims, and the spiritual force of a great civilization of which the world has need, is gathering at its back."

45\. Paragraph

Love of India was to Sri Aurobindo a religion, a spiritual experience. He once wrote that India and never been to him what was merely suggested by her outer vestures attractive and gorgeous though they are, She is to Him the Mother, the mother and minister-Mother, the compassionate, une mother of man. "Patriotism", wrote Sri Aurobindo, "cannot be anything short of a desire to redeem one's country. It cannot be to look upon the country as a repul- ture through it may seem so. It feels the immorality swirling beneath those ruins with which subjection has overgrown the country. It feels the pulsations of the im- mense eternal life of the country through the aromatic crust with which the great sleeper has been covered as with a shroud." Subjerton is an evil that eats into the vitals of a nation's being, grinding and es- roding its soul. It numbs therefore he must rid of it. It is the sight of a subject people, a 'charm', as it were, to free itself from the shackles of foreign rule. And sooner it is done the better. That is the only work

46\. Paragraph

WHO TRIUMPHS LAST!

47\. Image

The image is a black-and-white political cartoon by Shrikshart Hi. It depicts a hand holding a playing card labeled "INDIA" with a caricature of Mahatma Gandhi on it. The card is positioned above a table. On the table, there is a playing card showing the Ace of Spades, and another card showing the 6 of Spades. The cartoon uses these playing cards to represent India and its leaders, suggesting a commentary on the nation's political landscape. The artist's signature is visible in the bottom right corner.

48\. Paragraph

before the country, none greater than that "All expectation of moral regeneration which leaves freedom out of the count is a dream. First freedom, then regeneration... To recover possession of the State is there- fore the first business of the awakened Indian consciousness. If this is so, then it is obvious that the political liberation of India cannot be put off to a distant date as a thing which can be worked out at leisure, with the slow pace of the snail by opting degrees of semi caution. It must be done now. It is the first condition of life which must be satisfied if the nation is to survive."

49\. Paragraph

NOTHING BUT INDEPENDENCE When Diwanji Naoroji, as President of the Calcutta Congress, used the word SWARAJ to mean colonial self-government, Sir Auro- bindo's first pre-occupation was to declare openly for complete and absolute independ- ence as the aim of political action in India, and to insist on this persistently in the pages of the "Balade Mataram."

50\. Paragraph

He was the first politician in India who had the courage to declare this in public from 1946 onwards and he was immediately successful. The Congress under Nationalists leadership adopted is only in its Lahore session in 1929. And as the means to the attainment of sis and the 'Hindu Mataram' declared and developed a new political programme for the country as the programme of Nation- allist Party, including all the items of Sri Aurobindo's plan, already stated.

51\. Paragraph

Sri Aurobindo wrote a series of articles on positive restates, another developing the political philosophy of revolution. He also wrote many articles aimed at destroy- ing the shibboleths and superstitions of the Moderate Party, such as the belief in British justice and the benefits bestowed by foreign government on India, the faith in British law courts and in the adequacy of education given in schools and universities in India, and stressed more strongly and persistently than had been done the consecutioan, stagnation or slow progress, poverty, economic dependence, absence of rich industrial activity and all other evil results of a foreign government. He thala- ted especially that even if an alien rule were benevolent and beneficent that could not be a substitute for a free and healthy national life.

52\. Paragraph

Assisted by this publicity, the ideas of the Nationalists gained ground everywhere, especially in Bengal and the Punjab, which had before been predominantly moderate. The 'Randemataram' was almost unique in journalistic history in the influence it ex- ercised in converting the mind of a people and preparing it for revolution.

53\. Section Title

EXPLORING NEW PATTERNS

54\. Paragraph

But this was not his only work, because Sri Aurobindo, during these years, was un- tiringly active in his inner life, trying to explore newer paths to the supreme illumina- tion. And this does not mean that his outer activities were a thing apart from his inner life. They were indeed the practical application of the truths he realised in the inmost depths of his being. His thoughts and visions of the higher worlds of light found themselves incarnated in his work for the rehabilitation of his country's free- dom and greatness. He tells that India must be free so that he could do his spiritual work for her. All his activities, inward or outward, sprang from this conviction, and led towards the fulfilment of that deeper aim of his life.

55\. Paragraph

After the Suras debased Sri Aurobindo mat at Baroda the Mahatma Yoga Leto and had from him some guidance in yoga. The first result was a complete silence in the mind brought about in three days An emptiness overwhelmed him, so much so, that he might be unable to deliver a lec- ture at Bombay which he had already con- sented to do. But under the instructions of Leto he stood before the audience in that empty state of his mind and to and be- hold there came through him a regular stream of words, words of power and light that flowed out of his mouth. Keeping the audience spell bound. This silence has since remained in him and whatever he has written and said has all come direct from the higher planes of wisdom. A MEMORABLY LITURGICAL

56\. Paragraph

It was in that meeting that Sri Aurobindo made the memorable utterance: "Nations- ism is a religion that has come from God ....it has not been crushed. It is not go- ing to be crushed. Nationalism survives in the strength of God and it is not possible to crush it, whatever weapons are brought; agustus II. Nationalism is immortal; na- tionalism cannot die, because it is so human thing, it is God who is working in Bengal."

57\. Paragraph

The Government was then pursuing a policy of ruthless repression in order to suppress all Nationalist activities in Bengal. On his return to Calcutta Sri Aurobindo reiterated in the 'Handemataram': "Nationalism is itself no creation of individuals and can have no respect for persons: It is a force which God has created, and from Him it has received only one command, to advance and advance and ever advance until He bids it stop, because its appointed mission is done...Nationalism is an Avata-ra and cannot be slain. Nationalism is a divinely appointed shakti of the Eternal and must do its God-given work before it returns to the bosom of the Universal Energy from which it came."

59\. Paragraph

It was of this new and dynamic religion of nationalism that Sri Aurobindo was the inspired prophet and high-priest, whose mission was first to prepare the country for political freedom and then lead her to her great destiny of being the spiritual guide and teacher of the world by himself bring- ing down from heaven a new light for men, which will liberate him into a higher life, a divine perfection. He wrote: "India is the Guru of the nations, the physician of the human soul in its profounder mat- ters. She is destined once more to re- mould the life of the world and restore the peace of the human spirit. And Swaraj is the necessary condition of her work and before she can do the work, she must ful- fill the conditions."

60\. Paragraph

Sri Aurobindo has always felt that the movement of India's freedom was being guided by an Unseen Power and that she is bound to be free. He also knew that India has a secret Power which no other nation possesses, and that 'Our political beginning will have a religious end'. The change in his inner life which had already started was dependent on him when he was arrested and kept for sometimes in a solitary cell and then in jail during his trial. The days in the jail were for him

61\. Paragraph

spite of the fact that the conditions there were not as all favourable to earn pilgrims, VISION OF ALL KINSHINA

62\. Paragraph

In that Aahram, as he called the jail, he saw the vision of Sri Krishna every- where and in everything. He felt in him and about him the presence of Va- sudeva, his 'Friend and Lover.'

63\. Paragraph

Sri Aurobindo was not at all concerned about the prosecution: because he had been assuaged from within and knew that he would be acquitted. During this period his view of life was radically changed. He had taken up Yoga with the original idea of acquiring spiritual force and energy and divine guidance for the work of his life. Now now the inner spiritual life and reali- sation which had continually been in- creasing in magnitude and universality and assuming a large place took him up entirely and his work became a part and result of it and besides far exceeded the service and noeration of the country and fixed itself in an aim-previously only glimpsed which was worldwide in its bearing and concern- ed with the while future of humanity.

64\. Paragraph

Coming out of jail Sri Aurobindo resum- ed his political activity. He was determi- ned to continue the struggle. He held meet- ings in Calcutta and went out to places in the districts to speak. He started two jour- nals, one in Bengali called Dharma and the other in English called the Karmayogi- in', in both of which he re-emphasised his ideas with a greater force and from a new angle of vision. He wrote in the Kar- mayogini:

65\. Paragraph

"The problems which have troubled man- kind can only be solved by conquering the kingdom within, not by harnessing the forces of Nature to the service of comfort and luxury, but by mastering the forces of intellect and the spirit, by vindicating the freedom of man within as well as without and by conquering from within external Nature. For that work the resurgence of Asia is necessary, therefore Asia rises. For that work the freedom and greatness of India is essential, therefore she claims her destined freedom and greatness, and it is to the interest of humanity, not excluding England, that she should wholly establish her claim."

66\. Paragraph

He felt even more deeply than before that a higher Will was ruling itself in the striving of India for the recovery of her freedom and greatness and that he himself was an instrument of that Will. In fact after his return from jail he was always in a state of complete surrender to the Divine Will, He said in his Uttarpara speech: "I knew all along what He meant for me, for

67\. Paragraph

As regards the ideal of the Congress he repeated in the same letter his conviction with which he had started his political life. "Our ideal is that of Swaraj or absolute autonomy free from British control. We claim the right of every nation to live its own life by its own energies according to its own nature and ideals. We reject the claim of aliens to force upon us a civilisation inferior to our own or to keep us out of our inheri- tance on the untenable ground of a superior fitness..... The Swaraj matter can easily be settled by the substitution of 'full' and complete self-government for 'self-government on colonial lines' (the Moderate ideal) in the Swaraj resolution of the Congress."

68\. Paragraph

Minto-Morley reforms had come to sight, in this Sri Aurobindo grasped a develop- ment which he had always foreseen, the turn of Britain towards a more real move- ment of conciliation and concession in place of the mock reforms hitherto ob- served. Until now the motto of action for the Nationalist movement maintained by Sri Aurobindo had been "No Compro- mise" and its method as complete a non- co-operation as possible. But now we meet this change in the attitude of the Government he modified his formula. He wrote in an open letter to his countri- men, his Last Will and Testament: The policy of passive resistance was evoked partly as the necessary comple- ment of self-help, partly as a means of putting pressure on the Government. The essence of this policy is the refusal of co-operation as long as we are not ad- mitted to a substantial share and an effective control in legislation, finance and administration. Just as 'No repre- sentation, no taxation' was the waten- word of American constitutional agita- tion in the eighteenth century, so 'No control, no co-operation' should be the watchword of our lawful agitation-for constitution we have none-in the twen- teenth. We sum up this refusal of co- operation in the convenient word. Refus- al, refusal or co-operation in the in- dustrial exploitation of our country, in education in government, in judicial ad- ministration, in the details of social in- tercourse.

69\. Section Title

ANGER OF THE BRITISH

70\. Image

The provided image is a low-resolution, grayscale photograph that appears to be a historical or archival scan. It features a close-up of a person, likely a man, wearing glasses and a hat. The image is grainy, making fine details difficult to discern. A horizontal measuring stick or ruler is visible in the upper-left portion of the frame, spanning across the image. The background is indistinct and textured. As this is a photograph of a person and not a chart, graph, or plot, there is no quantitative data, axes, or legends to describe.

71\. Paragraph

Meanwhile, the British Government were hatching all sorts of plans either to deport Sri Aurobindo or to confine him in jail. Friends advised him to leave Bengal and carry on his work from outside. The trends of his inner life too were in favour of his withdrawal from

72\. Footnote

WAGED WAR OF INDEPENDENCE: Netaji Subhas Chandra Bose was snapped while addressing a gathering of 64,000 Indian soldiers who were prisoners of Japan at Singapore, appealing to them to join the Indian National Army.

73\. Paragraph

I heard it again and again, always I hear- ed to the voice within, "I am guiding, there- fore fear not. Turn to your own work for which I have brought you to fall and when you come out, remember never to lose, never to hesitate. Remember that it is I who is doing this, not eyes nor any other ......I am in the nation and its uplifting and I am Vasudeva, I am Narayana, and what I will, shall be, not what others will. What I choose to bring about no human power can stop."

74\. Paragraph

"RECOVER INDIANS FIRST." He called upon his countrymen to rediscover and repossess that priceless heritage and on that he build up the greater India of to-morrow "First there- fore become Indians Recover the pride- mony of your forefathers, RECOVER the Aryan thought, the Aryan discipline, the Aryan character, the Aryan life, RECOVER the 'Vedanta', the 'Gita', the 'Yoga'. Recover them not only in intellect or sentiment but in your lives. Live them and you will be great and strong, mighty, invincible and fearless.... For it is in the spirit that strength is eternal and you must win back the Kingdom of yourselves, the Inner Swarm, before you can win back your outer empire. There the Mother dwells and she waits for worship that she may give strength.

75\. Paragraph

"Believe in It, serve It, lose your wills in Hers, your ecstasies in the greater ego of the country, your separate self- consciousness in the service of humanity, Recover the source of all strength in yourselves and all else will be added to you, social soundness, intellectual pre- eminence, political freedom, the mastery of human thought, the regency of the world."

76\. Paragraph

These are words that clearly show how more and more inwards Sri Aurobindo was tending. The conviction was grow- ing upon him that the new India of the future could not be built on political freedom only. The race must awaken to its spiritual possibilities, to a pro- founder sense of its soul-realignment, for out of that knowledge alone can come the true vision and force of its self- development. In 1922 he wrote that he believed in a higher moral force as the one thing Indianness-the one thing that must be made active for the realization of India's freedom and great- ness.

77\. Paragraph

It was about this time (1909) that the

78\. Paragraph

active politics so that he could devote himself exclusively to that other work of his life, the work for the spiritual up- lift of India and there through of humanity. The command from above came that he should go to Chandanaggar and throw to Pondicherry. He was at that time certain that India would be free.

79\. Paragraph

In January, 1914, in the course of an interview to the representative of "India", a Tariff Nationalist weekly, Sri Aurobindo predicted that after a long period of wars, worldwide up- heavals and revolutions which were to begin in about four years, India would be on road to freedom.

80\. Paragraph

Sri Aurobindo's life of Yoga in Pondi- cherry has always been a mystery to the public and, indeed, it is so. For home knows how, living in "the vasta of God", he mastered the secret of a divine life upon earth towards the attainment of which he is no less mankind. And is not that divine life the meaning and mission of India's chequered existence through the ages?

81\. Paragraph

While utterly occupied with this stupendous work, Sir Aurobindo refused more than once request to preside at the sessions of the Indian National Con- gress. As his vision of the future grew clearer he saw that the eventual independ- ence of India was assured by the march of the forces of which he became aware; that Britain would be forced by the insalience of Indian demands and the pressure of international events to com- cede independence and that she was al- ready moving towards that eventuality with whatever opposition and reluct- ance.

82\. Paragraph

the fact that there would be no need of armed insurrection and that no secret preparation for it could be dropped without injury to the nation- als, even though the revolution- ary spirit had to be maintained and would be sustained in tact. His own personal intervention in politics would therefore be less longer inde- pendable. For the sake of his spir- itual work he kept his Ashram also free from all political action. Yet he abandoned his 'always'

83\. Paragraph

taking a very keen interest in the latter of the world and especially in the fate of India, he has kept himself in constant touch with them, but of course in his own way, and intervened, whenever accor-

84\. Paragraph

mary, to help or bid with his uttermost force.

85\. Paragraph

The aim of his Yoga is not only to realise the Divine beyond and attain to the highest spiritual consciousness, but also to take up all life and all world activity into the scope of the spiritual consciousness and action and to base them on the Truth of the Spirit and invest them with a spir- tual meaning. Hence the necessity of his keeping watch over the various activities of man all over the world.

86\. Paragraph

At first he used his spiritual force only to limited head of his work but after- wards he enlarged his orbit and began to act directly upon the world forces. Of the two occasions when he used his force and also publicly expressed his views, one was the Second World War during which he said in unequivocal terms that Hitler and his Nazi trans- sented dark Asiatic forces, that their success would mean the enslavement of mankind to the tyranny of evil, a definite set-back to the course of evolution and especially to the spiritual evolution of mankind and that it would lead also to the enslavement not only of Europe but also of Asia, and therefore of India, and the undoing of all the work they had been done for the later's liberation.

87\. Paragraph

It was for this reason that Set Achu- bindo advocated the Cripps Plan, be- cause by its acceptance India and Britain could have stood united against the Asiatic forces and the solution offered by Cripps could have been used as a step towards com- plete independence. The amibilation of Hitler and Nazism, and the finis- ment of Set Achubindo's provisions about the future of Indin are to-day facts that prove beyond doubt the victory of the spiritual force.

88\. Paragraph

LETTER TO C. R. DAS In 1923 in the course of his reply to a letter from Deshabandhu Chittaranjan Das, Sri Aurobindo wrote: "I see more and more manfully that man can never get out of the futile circle the race is always treading until he has raised himself on a new fund- ation. I believe also that it is the mission of India to make this great victory for the world. But what predestiny was the nature of the dynamic power of this great con- sciousness, what was the condition of its effective truth? How could it be brought down, mobilised, organised, turned upon life? How could our present instruments, intellect, mind, life, body be made true and perfect channels for this great transforma- tion? This was the problem I have been trying to work out in my own experience and I have now a sure basis; a wider knowl- edge and mastery of the secret."

89\. Paragraph

This dynamic power is the creative Force of God, the Light of the Supreme, which was glimpsed by the Wodit Bear and which was to come down on earth and newcreative man into a divine perfection, as rather to manifest the divinity which is already there in him, because that is his inherent dev- ity for the attainment of which Nature in him has been so constant travel India has stood through the ages to prepare per- self and the world for this ultimate end of man's terrestrial existence. All her past endevours are so many milestones on her path to that glorious consummation. Dr Aurobindo to-day has seen the supramach- tal Light, as he calls it, seen it in all its vastness, in all its supernatural splendour, and felt its invincible power or transfor- mation and new creation.

90\. Paragraph

Conditions in the world to-day show that the earth is becoming more and more ready for this Light to come down on it and be active in its consciousness and evolve out of man the Superman, even as man has evolved out of the animal. Indeed there are also signs of its coming. Mr Aurobindo therefore calls upon man to wake up from his agelong sleep in the ignorance and let up his eyes to catch the first golden glints of the descending glory. The descent of this new Light on earth he says would mean the beginning of the ascent of man from his present life of obscurity and fail- hood and death and suffering to the Supe- mental existence of Truth and Life and Life divine and the immortal's Ananda.

91\. Paragraph

This is the new world, the 'age of Gold', of which Sri Aurobindo dreamt in his childhood. This is the spiritual end of the political beginning as fore- seen by him when he was the leader of the Nationalist movement. This again will be the accomplishment of the work which he has been sent by God to do on earth by the power of Knowledge of that Light which is destined to bring to birth a new heaven and a new earth'. This will be the noontide of India's freedom and greatness of which Sri Aurobindo spoke in his early politi- cal writings.

92\. Paragraph

INDIA'S SPIRITUAL MISSION To reveal this truth so men may see and show him the way to his redemption is the spirit- ual mission for which India has lived throughout the ages and which she continues to-day through her greatest son. This is the final phase of Sri Aurobindo's work of which the earlier part was directed to the political freedom of India without which his spiritual work could not have been secure and fruitful.

93\. Paragraph

is it a mere coincidence that Sri Auro- bindo's birthday, the 19th of August, is also the day of India's independence? It is a day of great significance for India, which will crown her with the tender- ness of mankind. A new era of all human life is to night and it must begin with a spirit- ful awakening of wisdom this holy land will be the first centre. That is why the Sert to-day is also the Stranger of the Light who reveals the Veda "Sri". "Arise O Sages! arise!"

94\. Paragraph

അദ്ധ്യായം 1: ആമുഖം

95\. Paragraph

Books and Periodicals. Consists of "Sri Aurobindo, his life and work" in Bengali; French-G. Mundle-Hecquet (1946); Hindi-K. Srinivas Iyengar ("The Life Work of Sri Aurobindo"-J. C. Oehler). In English: The Life of Sri Aurobindo His Life and Works in Bengali by Prof. Chintamani Partha Sarathy Sastri published 1st edition Jan.-Feb., 1875.-In Telugu: Sri Aurobindo, His Life and Work in Kannada by K. V. Subba Rao published May, 1932.; in Tamil: Sri Aurobindo, His Life and Work in Malayalam by P. N. Panikkar published July, 1930. Unpublished letters of Sri Aurobindo to disciples are also included. "The Mother". Sri Aurobindo.

##### Layout understanding

Build a comprehensive representation of each page by understanding the semantic structure of the document.

0:00

-0:00

1×

### Source document

Input

![Malayalam newspaper: source document with bounding boxes](https://assets.sarvam.ai/tr:q-70,f-auto,dpr-auto/assets/products/doc-agents/samples/malayalam.webp)

Click a block to scroll to its text

### Akshar

Sarvam

Extracted blocks · 109 detected

1\. Header

ഗവണ്ണർ ഗിരിയുടെ വിടവാങ്ങൽ പ്രക്ഷോഭം ഇന്നു് (പി ടി ഐ) തിരു. മാ. 31 ഗവണ്ണർ മി. വി. വി. ഗിരി നാളെ വൈകുന്നേരം 8_45നും തിരുവനന്തപുരം-കോഴിക്കോടു നിലയത്തിൽ നിന്നും കേരളത്തിലെ ജനങ്ങൾക്കായി ഒരു വിടവാങ്ങൽ സന്ദേശം പ്രക്ഷോഭം ചെയ്യുന്നതായിരിക്കും. Reg: No K. 81 'തൊഴിലാളി' വരിസംഖ്യ നിരക്കു പോസ്റ്റ്ഫീ വാരാന്ത്യപ്പതിപ്പ് പോസ്റ്റ്ഫീ ഒരു കല്ലത്തേയ്ക്കും 27_00 6 മാസത്തേയ്ക്കും 13_50 1 മാസത്തേയ്ക്കും 2_25 ഏജൻറുമാർവഴി ഒരു മാസത്തേയ്ക്കും വാരാന്ത്യപ്പതിപ്പ് അടക്കം 2_10 ഒറപ്രതി 0_07 ഓറപ്രതി 0_07 വാരാന്ത്യപ്പതിപ്പ് അടക്കം 2_10 മാനേജർ. 0_10 പേജ് 4 Founder: Father Vadakkan Honourary Chief Editor T. O. Mathew M. A. Managing Editor B. Wellington B. A. പുസ്തകം 12 | ലക്കം 88 | ഏപ്രിൽ 1 വ്യാഴം | തൃശൂർ | വില 7 പൈസ | പേജ് 4

2\. Headline

പ്രതികാരത്തിന്നു് അമേ രിക്ക പുകയുന്നു

3\. Headline

അബ്ദുള്ള ചൈന കാണില്ല പ്രധാന മന്ത്രി ശാസ്ത്രിയുടെ സുദൃഢ പ്രഖ്യാപനം

4\. Paragraph

ഷെയ്ക്ക് ചൈന സന്ദർശിച്ചാൽ ശക്തമായ നടപടി എടുക്കുമെന്ന് സ്വരൺസിങ്ങും

5\. Paragraph

(പി. ടി. ഐ)

6\. Paragraph

ചൈനയിലേക്കു് പോകുവാൻ ഷെയ്ക്ക് ഗവമ്മെണ്ടു് ഒരിക്കലും അനുവദിക്കുകയില്ലെന്നു ഇന്ന് ലോകസഭയിൽ പ്രഖ്യാപിച്ചു.

7\. Paragraph

ഗവണ്മെൻ്റിൻ്റെ ഈ നിലപാട് ഷെ യ്ക്ക് അബ്ദുള്ളക്ക് വ്യക്തമാക്കി കൊ ടുക്കണമെന്നും അദ്ദേഹം തുടർന്നു പറഞ്ഞു.

8\. Paragraph

ഈ പ്രശ്നത്തെ സംബന്ധിച്ച് വിദേ ശകാര്യമന്ത്രി സ്വരൺസിങ്ങും നേര ത്തെ നല്ലിയ മറുപടി അതൃപ്തികരമാ ണെന്നും ഏതാനും പ്രതിപക്ഷ അംഗ ങ്ങൾ ചൂണ്ടിക്കാണിച്ചതിനെ തുടർന്നാ ണു് പ്രധാനമന്ത്രി ഈ ഉറപ്പ് കൊടു ത്തത്.

9\. Sub-headline

അൽബേനിയായിൽ

10\. Paragraph

ചൈനയിലേക്ക് പോകുന്നതും ഷെ യ്ക്ക് അബ്ദുള്ളക്ക് അഭിലഷണീയമാ ണെന്നു തങ്ങൾക്കു തോന്നുന്നില്ലെന്നും, ഗവമ്മെണ്ടിന്നും ഇ ക്കാ ര്യ ത്തി ലു ള്ള ശക്തിയായ അഭിപ്രായങ്ങൾ ഷെയ്ക്ക് അബ്ദുള്ളയെ അറിയിക്കുമെന്നുമാണു സർദാർ സ്വരൺസിങ്ങും നേരത്തെ പറഞ്ഞതു്.

11\. Section Title

പാസ്പോർട്ട് എന്തിന് കൊടുത്തു?

12\. Paragraph

വിദേശപര്യടനത്തിന്നായി ഷെയി ക്ക് അബ്ദുള്ളക്ക് 35000 ഉറുപ്പികയുടെ വിദേശനാണ്യം കൊടുത്തതു് എന്തിനാ ണെന്നും അംഗങ്ങൾ ചോദിച്ചു. ഒരു കാഷ്ടീരി മുസ്ളീമാണ് താനെന്നും അബ്ദുള്ള പറഞ്ഞ സ്ഥിതിക്ക് എത്തി നാണു് ഒരു പാസ്സ്പോർട്ട് കൊടുത്ത തെന്നും അവർ ചോദിച്ചു.

13\. Paragraph

ഈ കാര്യത്തെസംബന്ധിച്ചു രാജ്യ സഭയിലും ലോകസഭയിലും ഗവണ്മെണ്ടു വക്താക്കൾ നൽകിയ പ്രസ്താവനകൾ വിഭിന്നമാണെന്നുള്ള ഹെംബറുവയുടെ പോയിൻറ് ഓഫ് ഓർഡർ സ്പീക്കർ തള്ളിക്കളഞ്ഞു.

14\. Paragraph

പാക്ക് ഗവമ്മേണ്ടുമുഖേന നല്ലിയ ചൈനീസ് ഗവമ്മെണ്ടിന്റെ ക്ഷണം ഷെയ്ക്ക് അബ്ദുള്ള സ്വകരിച്ചതാ യി ഗവമ്മെണ്ടിന്നും അറിവില്ലെന്നും വിദേശകാര്യമന്ത്രി സ്വരൺസിങ്ങ പറഞ്ഞു. ചൈനയിലേക്ക് പോകുന്ന തിന്നുള്ള ഒരു പാസ്പോർട്ട് ഷെയി ക്ക് അബ്ദുള്ളക്ക് നല്കിയിട്ടില്ല.

15\. Paragraph

ചൈനയിലേക്കു് പോകുവാൻ അനു വദിക്കുകയില്ലെന്നുള്ള പ്രധാനമന്ത്രിയു

16\. Paragraph

ന്യൂഡൽഹി, മാച്ച് 31 അബ്ദുള്ളയെ ഇന്ത്യാ പ്രധാനമന്ത്രി ശാസ്ത്രി

17\. Paragraph

ടെ പ്രഖ്യാപനം ഉള്ളപ്പോൾതന്നെ അബ്ദുള്ള ചൈന സന്ദർശിക്കുകയാ ണെങ്കിൽ ഗവണ്മെണ്ടു് എന്തു നടപടി യാണു് എടുക്കുകയെന്നും അംഗങ്ങൾ ആരാഞ്ഞ.

18\. Section Title

ക്ഷണം സ്വീകരിച്ചാൽ

19\. Paragraph

ചൈനയുടെ ക്ഷണം സ്വീകരിക്കുക യാണെങ്കിൽ അബ്ദുള്ളയെ രാജ്യരക്ഷാ നിയമമനുസരിച്ചു അറസ്റ്റ് ചെയ്യുമെ ന്നും, വീണ്ടും തടങ്ങലിൽ വെക്കുമെന്നും ഗവണ്മെണ്ടു് അബ്ദുള്ളയോടു് പറഞ്ഞി ട്ടുണ്ടായെന്നും എസ്. എം. ബാനർജി ചോദിച്ചു.

20\. Paragraph

ചൈന സന്ദർശിക്കുകയാണെങ്കിൽ അ ബ്ദുള്ളയുടെ ഇന്ത്യയിലേക്കുള്ള തിരി ച്ച വരവ് നിരോധിക്കുമെന്നേ ഹേം ബരവ ചോദിച്ചു.

21\. Paragraph

ഇതിന്നും ഉത്തരമായി സ്വരൺസി ങ്ങ് പ്രധാനമന്ത്രിയുടെ സുദൃഢപ്രഖ്യാ പനത്തിലേക്ക് അംഗങ്ങളുടെ ശ്രദ്ധയെ ക്ഷണിച്ചു. അബ്ദുള്ള ചൈന സന്ദശി ക്കുകയാം.ണങ്കിൽ സ്ഥിതിഗതികൾക്ക നുസരിച്ചു് എന്തു് നടപടിയാണു എ ടു ക്കേണ്ടതെന്നു് അ പ്പോൾ തീരുമാനിക്കും. ഹേംബറവ

22\. Paragraph

നിർദ്ദേശിക്കുന്ന നടപടി വളരെ മയമു ള്ളതാണു്. അതിൽ കൂടുതലായി നടപ ടികൾ എടുക്കേണ്ടിവരുമെന്നും സ്വര ൺസിങ്ങ് പറഞ്ഞു.

23\. Paragraph

നടപടി എടുക്കണമെന്നു് തീർച്ച

24\. Paragraph

ചില ചുററുപാടുകളിൽ എന്തു നടപ ടിയാണു് എടുക്കുകയെന്നു മുൻകൂട്ടി പ റയുവാൻ സാദ്ധ്യമല്ല. എന്തു നടപടി യാണു് എടുക്കേണ്ടതെന്നും അവസരം വരുമ്പോൾ തീരുമാനിക്കമെന്നും വിദേ ശകാര്യമന്ത്രി വ്യക്തമാക്കി.

25\. Paragraph

പാക്ക് ഗവണ്മെണ്ടു് മുഖേന ഷെയ് ക്കും അബ്ദുള്ളയെ ചൈന ക്ഷണിച്ചതു തികച്ചും അസാധാരണമാണു്. ചൈന യും, പാക്കിസ്ഥാനും ഇപ്പോൾ ഒത്തുചേ ന്നും പ്രവർത്തിക്കുകയാണു്. ചൈനീസ് ക്ഷണം ഷെയിക്ക് അബ്ദുള്ളക്ക് നൽ കിയ പാക്കിസ്ഥാൻ്റെ നടപടിയിൽ പ്രതിഷേധിച്ചതുകൊണ്ടു് പറയത്തക്ക പ്രയോജനമുണ്ടെന്നു തോന്നുന്നില്ലെന്നും സ്വരൺസീങ്ങ് പ്രസ്താവിച്ചു.

26\. Headline

അയ്യൂബ് ഖാൻ എന്ന ചെറ

27\. Headline

ചൌഎൻലായി തുര പ്പൻപണി നടത്തുന്ന

28\. Paragraph

ചൈനീസ് പ്രധാനമന്ത്രി ചെൻലിയായിയും അർജീരിയൻ പ്രധാനമന്ത്രി ബെൻബെല്ലയും ഒരു ഔ പചാരിക ചർച്ച പരമ്പര ഇവിടെ ആരംഭിച്ചിരിക്കു ന്നു.

29\. Section Title

ചീനക്കവേണ്ടി പാക്ക് പ്രമാണിയുടെ വക്കാലത്ത് [പി. ടി. ഐ] കറാച്ചി, മാച്ച് 31

30\. Paragraph

ആഫ്രോഏഷ്യൻ പ്രശ്നങ്ങൾ മൊത്ത ത്തിലും ദക്ഷിണ പൂർവേഷ്യൻ പ്രശ്നം പ്രത്യേകിച്ചും അവരുടെ ചർച്ചയ്ക്കു വി ധേയമാകുമെന്നറിയുന്നു.

31\. Headline

അരജിയേഴ്സിൽ തിരക്കിട്ട ചർച്ച

32\. Paragraph

റൈനക്ക് കൂടുതൽ പ്രദേശങ്ങളൊ ജനങ്ങളൊ ആവശ്യമില്ല. ഇവ രണ്ടും ചൈനയ്ക്കും വേണ്ടത്രയുണ്ടു്. ചൈനത ന്നെ ഒരു വലിയ രാഷ്ട്രമാണു്. വമ്പിച്ച

33\. Paragraph

'ചൈനീസ് ഭീഷണിയുടെ വ്യാജേന, വിദേശങ്ങളിൽനിന്നും ഇന്ത്യ സൈ നികസഹായം തേടു"ന്നതിനെ പ്രസിഡണ്ടും അയൂബ്ഖാൻ വീണ്ടും കുററപ്പെടുത്തിയിരിക്കുന്നു

34\. Paragraph

രണ്ടു ദിവസത്തെ ഔദ്യോഗിക സന്ദ ർശനം ഇന്നലെ ഇവിടെയെത്തിയ ചൌവിനെ ബെൻബെല്ലയും ഭരണക ക്ഷിതാക്കളും ചേർന്നു സ്വീകരിച്ചു.

35\. Paragraph

വഴിയിൽ ഒരു സ്വീകരണത്തിൽ പങ്കെടുക്കകൊണ്ടും സംസാരിക്കുക യായിരുന്നു അദ്ദേഹം.

36\. Paragraph

'അമേരിക്കൻ സാമ്രാജ്യത്വത്തിനും അതിൻറെ അക്രമണോപകരമായ ഇ സ്രായേലിനും' എതിരായി അറബിജന ത നടത്തുന്ന പോരാട്ടത്തിനും ചൌ പി ന്തുണ വാഗ്ദാനം ചെയ്തു. ഇതിനു പു റമെ പാലസ്തീനിലെ അറബികൾക്കും യെമൻ, ഓമാൻ, കോങ്കോ എന്നിവിടട ങ്ങളിലെ ജനങ്ങൾക്കും ചൌ പിന്തുണ പ്രഖ്യാപിച്ചു.

37\. Paragraph

ദക്ഷിണ വിയറ്റ്നാമിലെ അമേരി ക്കൻ നിലപാട് സ്വീകാര്യമല്ലെന്നും ചൌ പറഞ്ഞു. അതു് ജനീവാ കരാ രിനു വിരുദ്ധമാണു്. 'ടിറേറായിസ്റ്റ് യുഗോസ്ളാവ്ക്ലിക്കും' അല്ലാതെ മററാ രും ഇക്കാര്യത്തിൽ സമാധാനപരമായ കൂടിയാലോചന വേണമെന്നു പറയുക യില്ല. വിയാറ്നാം ജനത ആയുധം വെച്ചു കീഴടങ്ങണമെന്നാണു അതി ൻറ യഥാർത്ഥ അർത്ഥം.

38\. Paragraph

ചൌ പ്രസംഗിക്കുന്നതിനു മുമ്പ് അ ൽബേനിയൻ പ്രധാനമന്ത്രി മെഹമെ ത് ചേഹൌ 'ക്രൂഷേവിൻറെ പിൻഗാ മികളെ' ശക്തിയായി വിമശിച്ചുകൊ ണ്ടു് പ്രസംഗിക്കുകയുണ്ടായി.

39\. Paragraph

ജോൺസൺ ചെയ്യുന്നുണ്ടു്. ജോൺ സൺ ഭരണകൂടം യുദ്ധക്കൊതി പൂണ്ടതാണെന്നും അതിൻ്റെ നടപടി കൾ സ്ഥിരീകരിച്ചിരിക്കുന്നു.

40\. Ad

ലക്ഷ്മി ഓയിൽമിൽ പൂങ്കുന്നം :: തൃശൂർ എന്റെ വക പൂങ്ങുന്നത്തുള്ള ഓയിൽമില്ലിൽനിന്നും ഇന്നു (1-4-'65) മുതൽ നല്ലെണ്ണയും, പിണ്ണാക്കും മൊത്ത മായും, ചില്ലറയായും മിതമായ വിലയ്ക്ക് വില്ക്കുന്നവിവരം പൊതുജനങ്ങളെ അറിയിക്കുന്നതോടൊപ്പം, നിങ്ങളുടെ വില യേറിയ സഹകരണങ്ങൾ പ്രതീക്ഷിച്ചുകൊള്ളുന്നു. കൂടാതെ ¼, ⅓ ടിന്നുകളിലായും, കുപ്പികളിലായും സീൽ ചെയ്ത് നല്ലെണ്ണ വില്പനയ്ക്കുണ്ടാകുന്നതാണു്. എന്നു', ലക്ഷ്മി ഓയിൽ മിൽ, പൂങ്കുന്നം, തൃശൂർ_2 പ്രൊപ്രൈററർ: എം. സുന്ദരംചെട്ടിയാർ

41\. Ad

തൃശൂർ ഫുട്ബോൾ ടൂർണ്ണമെൻറ് 9-ാം വാഷികം ഇന്നും 1_4_65 വ്യാഴാഴ്ച 5_15നും പാലസ്സ്റ്റേഡിയത്തിൽവെച്ച് വാശിയോടെ പെരുതി സമനിലയിൽ പരിഞ്ഞ ആ കളി വീണ്ടും പഞ്ചാബ് പോലീസ് V/s എ. ഓ. സി. സെന്റർ പഞ്ചാബ് സെക്കണ്ടറബാദ് നിരക്കുകൾ } ഗ്യാലറി 0_60 പ. പടിഞ്ഞാറം തെക്കും കസേര 1_00 } 0_40 പ. കിഴക്ക്

42\. Paragraph

അടുത്തുവരുന്ന ആഫ്റോ-ഏഷ്യൻ സമ്മേളനത്തിൽ സോവിയറ്റ് യൂണി യനും മലയേഷ്യയും പങ്കെടുക്കുന്നതി നെ തടയാൻ അൾജീരിയയെ നിബ്ബ ന്ധിക്കുകയെന്നതാണു് ചൌവിൻറ സന്ദശനലക്ഷ്യങ്ങളിൽ പ്രധാനമായ തെന്നും നയതന്ത്രവൃത്തങ്ങൾ വിശ്വസി ക്കുന്നതായി പി. ടി. ഐ.യുടെ സ്മാഫം പ്രതിനിധി സി. രാഘവൻ എഴുതുന്നു. അൽബേനിയായിൽ

43\. Image

? Await Opening

44\. Paragraph

ഹൈദ്രബാദ്, മാ. 31 സ്റ്റേററ് ഹൌസിങ്ങ് ബോർഡി ൽനിന്നും പണിയിച്ച വീടുകൾ ആ വശ്യമായ വിജ്ഞാപനങ്ങൾ കൂടാ തെ ലഭിച്ചവർ അവ ഹൌസിങ്ങ് ബോർഡിന്നുതന്നെ ഒഴിഞ്ഞുകൊടു ക്കേണ്ടതാണെന്നും മുഖ്യമന്ത്രി കെ. ബ്രഹ്മാനന്ദ റെഡ്ഡി ഇന്നലെ നിയ മസഭയിൽവെച്ച് പ്രസ്താവിച്ചിരി ക്കുന്നു. ഇങ്ങിനെ വീടുകൾ ഒഴിയേ ണ്ടവരുടെ കൂട്ടത്തിൽ മുഖ്യമന്ത്രിയു ടെ ഭാര്യ, കേന്ദ്ര ഉരുക്കുമന്ത്രി എൻ. സഞ്ജീവ റെഡ്ഡിയുടെ ഭാര്യ, അദ്ദേ ഹത്തിൻറെ ജാമാതാവ് എന്നിവർ ഉൾപ്പെടുന്നു.

45\. Paragraph

സംസ്ഥാനത്തെ പ്രതിപക്ഷ പാർ ട്ടികളുടെ ത്രക്ഷമായ വിമർശനത്തി ന്നും വിധേയമായ ഒരു പ്രശ്നമായി രുന്ന ഇത്.

46\. Paragraph

'64_'65ലേക്കുള്ള ഉപധനാഭ്യർത്ഥ നകളെക്കുറിച്ചുള്ള ചർച്ചകൾക്ക മറുപടി പറയുന്നതിനിടയിലാ ണ് മുഖ്യമന്ത്രി ഇപ്രകാരം പ്രസ്താ വിച്ചത്.

47\. Paragraph

ജനസംഖ്യയും. ഒരു സാഹചര്യത്തിലും ഇന്ത്യയെ പിടിച്ചടക്കുകയും അങ്ങനെ 40 കോടി ജനങ്ങളെക്കൂടി തീററിപ്പോ റരുന്ന ഉത്തരവാദിത്വം ഏറെറടുക്കുക യും ചെയ്യുന്നതിന്നും ചൈന അഭിലഷി ക്കുന്നില്ല.

48\. Paragraph

Global Trades & Industries.

49\. Paragraph

ചീനയോട് മമത പുലർത്തുന്ന അൽ ബേനിയായിൽ നിന്നാണു് ചൌ ഇവി ടെയെത്തിയതു്. ജോൺസൺ ഭരണ ത്തിൻറെ പാതകങ്ങൾ അതിൻറെ മുൻ ഗാമികളുടേതിനേക്കാൾ കാടത്തം നി റഞ്ഞതാണെന്നും ചൌഎൻലായി ത ലസ്ഥാനമായ ടിറാനയിൽവച്ച് പാ ഞ്ഞ ഐസനോവരും കെന്നഡിയുംചെ യ്യാൻ ധൈര്യപ്പെടാതിരുന്ന കാര്യങ്ങൾ

50\. Paragraph

കാശ്മാർ പ്രശ്നത്തെ പരാമർശിച്ചുകൊ ണ്ടും അദ്ദേഹം ഇങ്ങനെ പറഞ്ഞു. ഈ പ്രശ്നം സമാധാനപരമായി പരിഹരി ക്കുന്നതിന്നും പാക്കിസ്ഥാൻ സദാ ശ്രമി ച്ചുപോന്നിട്ടുണ്ടു്. എന്നാൽ, സൌഹാദ്ദ പരമായി ഈ പ്രശ്നം പരിഹരിക്കേണ്ട ന്നതിൻറെ അടിയന്തിരാവസ്ഥയെപ്പറ്റി ഇതുവരെ ഇന്ത്യൻ നേതാക്കൾക്കു ബോ ധ്യം വന്നിട്ടില്ല.

51\. Paragraph

എല്ലാ അന്തർദേശീയ പ്രശ്നങ്ങളും ശ ക്തിയും ആക്രമണവുംകൊണ്ടു് പരിഹ രിക്കണമെന്നതാണു് ഇന്ത്യയുടെ അഭി ലാഷം. ഈ നയമാണ് അവർ കഴി ഞ്ഞകാലത്തെല്ലാം അനുവർത്തിച്ചുപോ ന്നിട്ടുള്ളതു്. ഇപ്പോഴും ഇന്ത്യ അതി ന്മേൽതന്നെ തൂങ്ങിപ്പിടിച്ചുകിടക്കുകയാ ണെന്നും അയൂബ്ഖാൻ പറഞ്ഞു.

52\. Paragraph

ഇന്ത്യയുടെ ഭാഗത്തുനിന്നുമുള്ള ഈ ആക്രമണാസക്തമായ സമീപനം, കഴി ഞ്ഞകാലത്തേക്കാൾ രൂക്ഷമായിരിക്കുക യാണത്രെ. മററു രാഷ്ട്രങ്ങളിൽനിന്നും വമ്പിച്ച തോതിലുള്ള സൈനികസഹാ യം ലഭിക്കുന്നതിനെ തുടന്നാണ് ഈ സമീപനത്തിന്നു് രൂക്ഷത വദ്ധിച്ചതെ ന്നും അദ്ദേഹം പറഞ്ഞു,

53\. Section Title

സൂത്രത്തിൽവീട്ടടങ്ങിയ മന്ത്രി പത്നിമാരെ കടിയിറക്കുന്നു

54\. Paragraph

പാക്കിസ്ഥാൻ്റെ വിദേശനയം വ്യ ക്തമാണു്. മനസ്സിലാക്കുവാൻ എളുപ്പ വുമാണു്, ഞങ്ങൾ സമാധാനമാണു ആഗ്രഹിക്കുന്നതു്. ആരുമായി സമാ ധാനത്തിൽ കഴിയുന്നതിന്നും ഞങ്ങൾ അഭിലഷിക്കുന്നു. തെറ്റിധരിപ്പിക്ക പ്പെടാവുന്ന യാതൊന്നും പാക്കിസ്ഥാൻ നയത്തിലില്ലെന്നും അയൂബ്ഖാൻ അവ കാശപ്പെട്ടു

55\. Section Title

കർട്ടനാൾ മൊറീലിയോ ഫൊസാറി അന്തരിച്ചു.

56\. Paragraph

(പി. ടി. ഐ.) ഡാക്ക, മാ. 31 കിഴക്കൻപാകിസ്ഥാൻറയും പശ്ചി മബംഗാളിൻറെയും അതിർത്തിയിലുള്ള രങ്കപ്പൂർ-കൂച്ചുബിഹാർ പ്രദേശത്തും ഇ ന്നു വൈകിട്ട് അഞ്ചുമണിക്കും വെടി നിർത്തൽ പ്രാബല്യത്തിൽ വന്നിരി ക്കുന്നു.

57\. Section Title

വെടിനിർത്തൽ നടപ്പിൽവന്നു

58\. Paragraph

(എ. എഫ്. പി.) വത്തിക്കാൻ സ്പെറി

59\. Paragraph

പാകിസ്ഥാനിലെ ഇന്ത്യൻ ഹൈക്ക മ്മീഷണർ ജി. പാത്ഥസാരഥിയും കി. പാകിസ്ഥാൻ ചീഫ്സെക്രട്ടറി അലി അഷ്ഗാരം ഇന്നലെ ഇവിടെവച്ചു നട ത്തിയ ചച്ചയിൽ വച്ചാണു് ഇതുസംബ ന്ധിച്ച തീരുമാനമുണ്ടായത്. ന്യൂഡൽ ഹിയിലെ പാക് ഹൈക്കമ്മീഷണർ അർഷദ് ഹുസൈനും യോഗത്തിൽ സംബന്ധിച്ചിരുന്നു.

60\. Headline

കോൺഗ്രസ്സിനും കേവല ഭൂരിപക്ഷമില്ല

61\. Paragraph

വത്തിക്കാൻ സിററി, മാ. 30 ടൂറിനിലെ ആർച്ച് ബിഷപ്പ് കർദ്ദീ നാൾ മൊറീലിയോ ഫൊസാററി ടൂറി നിൽവെച്ചും അന്തരിച്ചിരിക്കുന്നു. അദ്ദേ ഹത്തിന്നു 89 വയസ്സ് പ്രായമുണ്ട്. കർദ്ദിനാൾ ഫൊസാറ്ററിയുടെ മര ണത്തോടെ കർദ്ദിനാൾ തിരുസംഘ ത്തിൻറെ അംഗസംഖ്യ നൂറായി കുറ ഞ്ഞിരിക്കുന്നു. ഇതിൽ 27 ഇറ്റലിക്കാ രും 72 ഇതരരാജ്യക്കാരുമാണു്.

62\. Section Title

കൽക്കത്ത കോർപ്പറേഷൻ തെരഞ്ഞെടുപ്പു ഫലം

63\. Paragraph

(പി ടി ഐ) കൽക്കത്ത, മാർച്ച് 31

64\. Paragraph

കൽക്കത്ത മുൻസിപ്പൽ കോർപ്പറേഷനിലേക്ക് നടന്ന തെര

65\. Paragraph

തെരഞ്ഞെടുപ്പിൽ ഭരണകക്ഷിയായ കോൺഗ്രസിനു് ഇത്ത വണ കേവല ഭൂരിപക്ഷം കിട്ടിയതും.

66\. Paragraph

തെരഞ്ഞെടുപ്പ് ഫലങ്ങൾ ഇന്നുരാ വിലെ പ്രഖ്യാപിച്ചു. കൗൺസിലിൻറ അംഗസംഖ്യ ആറാണ്. പ്രായപൂർത്തി വോട്ടവകാശത്തിൻറെ അടിസ്ഥാനത്തി ൽ ആദ്യമായി കൗൺസിലേക്കും തെര ഞ്ഞെടുപ്പ് നടന്നതും കഴിഞ്ഞ ഞായറാ ഴ്ചയാണു്. 289 സ്ഥാനാർത്ഥികൾ മൊ ത്തം മത്സരിച്ചിരുന്നു.

67\. Paragraph

കക്ഷിനില ഇതാണു്:

68\. Paragraph

തോറ്റവരിൽ ഒരാൾ മുൻ ഡെപ്യൂ ട്ടി മേയർ തുളസീചരൻപാൾ ആണു്. കോൺഗ്രസിൻറെ പിന്തുണയോടു കൂടി സ്വതന്ത്രനായിട്ടാണു് അദ്ദേഹം മത്സരി ച്ചതു്. തെരഞ്ഞെടുക്കപ്പെട്ട 6 യു. സി. സി. സ്ഥാനാർത്ഥികളും, പ്രോഗ്രസ്സീവ് സിററിസൺസ് ബ്ലോക്കിന്റെ ഒരു സ്ഥാനാർത്ഥിയും തടങ്ങലിലാണ്.

69\. Paragraph

കോൺഗ്രസ്_49, യുനൈറഡ് സിററിസൺസ് കമ്മറ്റി_34, പ്രോഗ്ര സീവ് സിററിസൺസ് ബ്ലോക്ക്_5, ജനസംഘം_1, സ്വതന്ത്രന്മാർ_11

70\. Paragraph

കോൺഗ്രസ് എല്ലാ സീററുകളിലും മത്സരിക്കുകയുണ്ടായി. കമ്യൂണിസ്റ്റ്പാ ട്ടി (ഇടതും, വലതും) റവലൂഷനറി കമ്മ ണിസ്റ്റ് പാർട്ടി, റവലൂഷനറി സോഷ്യ ലിസ്റ്റ് പാർട്ടി, ഫോർവേഡ് ബ്ലോക്ക് (മാർക്സിസ്റ്റ്), വക്കേഴ്സ് പാർട്ടി എ ന്നീ കക്ഷികൾ ചേർന്നുകൊണ്ടുള്ള യു.

71\. Section Title

2nd Death Anniversary

72\. Image

ചിത്രം ഒരു പഴയ കറുപ്പും വെളുപ്പും ഫോട്ടോയാണ്. ഇതിൽ ഒരു പുരുഷന്റെ ചിത്രം കാണാം. അദ്ദേഹം ഒരു വെള്ള ഷർട്ട് ധരിച്ചിരിക്കുന്നു. ചിത്രത്തിന് ഒരു തരി രൂപമാണുള്ളത്.

73\. Paragraph

Rev. Fr. S. M. THATTIL; M A. BORN 19_3_1898 DIED 1_4_1963 Inserted By MATHAI JOS ANDREWS

74\. Paragraph

സി. ഡി. 87 സ്ഥാനാർത്ഥികളെ രംഗ ത്ത് ഇറക്കിയിരുന്നു. അവരിൽ 8 പേർ സ്വതന്ത്രരാണെ.

75\. Paragraph

എസ്. എസ്. പിയും, ഫോർവേ ഡ് ബ്ലോക്കും ചേർന്നുകൊണ്ടുള്ള പ്രോ ഗ്രസ്സീവ് സിററിസൺസ് ബ്ലോക്ക് 12 സ്വതന്ത്രന്മാരടക്കം 40 സ്ഥാനാ ത്ഥികളെ നിർത്തുകയുണ്ടായി. സോഷ്യ ലിസ്റ്റ് യൂനിററി സെൻററിന്നും (യു സി. സിയിൽനിന്നും തെറ്റിപ്പിരിഞ്ഞ തു) നാല് സ്ഥാനാർത്ഥികൾ ഉണ്ടായിരു ന്നു. ബാക്കിയുള്ള സ്ഥാനാർത്ഥികൾ ഒരു പാർട്ടിയുടേയും പിന്തുണയില്ലാത്ത സ്വ തന്ത്രന്മാരായിരുന്നു.

76\. Paragraph

മുൻ കൗൺസിലിലെ കക്ഷിനില ഇ തായിരുന്നു കോൺഗ്രസ്_47, യു. സി സി_24, പി. സി. ബി_4, സ്വതന്ത്ര ന്മാർ_3, രണ്ടു് സീററുകൾ ഒഴി ഞ്ഞകി ടക്കുകയായിരുന്നു.

77\. Section Title

മട്ടവിഷമെന്ന മരണം

78\. Paragraph

(പി. ടി. ഐ) മദ്രാസ് മാ. 31 18 വയസ്സിന്നും മേലെയുള്ളവക്കും മാത്രമേ മൂട്ടവിഷം വില്ക്കുവാൻ പാടുള്ളുവെന്ന ഗവണ്മെണ്ടിൻറ ചട്ടം അസാധാരണമായ ഒന്നാ ണെന്നും സ്വതന്ത്രമെമ്പർ ഗണേ ശൻ ഇന്നും മദ്രാസ് നിയമസഭ യിൽ പ്രസ്താവിച്ചു.

79\. Paragraph

വാസ്തവം പറഞ്ഞാൽ 18 വയ സ്സ് കഴിഞ്ഞവരാണ് ആത്മഹ ത്യയെപ്പറ്റി ചിന്തിക്കുന്നത്.

80\. Paragraph

മൂട്ടവിഷം മൂട്ടകൾക്ക് മാരക വും, മനുഷ്യക്ക് നിരുപദ്രവവും ആക്കുന്നതിന്നുള്ള വല്ല മാർഗ്ഗവും കണ്ടുപിടിക്കണമെന്നും അദ്ദേഹം നിർദ്ദേശിച്ചു.

81\. Section Title

കമ്മ്യൂ. എംബസ്സി കട്ടനാളിനു ഡിന്നർ സല്ക്കാരം നല്ലത്

82\. Section Title

വെടിനിർത്തൽ പ്രാബല്യ ത്തിൽ വരുമെന്ന് സ്വരൺസിങ്ങ്

83\. Paragraph

റോം_മപ്പാപ്പാ തിരുമേനി ഈ യിടെ നിയമിച്ച 27 കർദ്ദിനാളന്മാ രിൽ ഒരാളായ കരദ്ദിനാൾ സെപ്പര തിരുമേനിയുടെ ബഹുമാനാത്ഥം റോമിലെ യുഗോസ്ളാവ് എംബ സ്സി ഒരു ഡിന്നർ സല്ക്കാരം നടത്തി യിരിക്കുന്നു.

84\. Paragraph

ഇന്ത്യയുടേയും പാക്കിസ്ഥാൻറെയും ഹൈക്കമ്മീഷണർമാർ ഇന്നലെ വൈ കുന്നേരം ഡാക്കയിൽ നടത്തിയ ചച്ച കളുടെ ഒരു റിപ്പോർട്ട് ഇതുവരെ ഗവ മ്മെണ്ടിന്നു ലഭിച്ചിട്ടില്ലെങ്കിലും കൂച്ച്- ബീഹാർ അതിർത്തിയിൽ വെടിനിർത്തൽ ഇന്നും ഉച്ചയ്ക്കുശേഷം പ്രാബല്യത്തിൽ വരുമെന്നകാര്യം വ്യക്തമാണെന്നു വിദേ ശകാര്യമന്ത്രി സർദാർ സ്വരൺസിംഗ് ഇന്നും രാജ്യസഭയിൽ പറഞ്ഞു. മി. ഡി. സെൻഗുപ്തയും മററു ആറ

85\. Paragraph

സല്ക്കാരത്തിൽ പങ്കെടുത്ത അതി ഥികളിൽ കർദ്ദിനാൾ ടിസ്സരാ ങ്ങ്, അസാധാരണ സഭാകാര്യങ്ങളു ടെ വത്തിക്കാനിലെ അണ്ടർ സെ ക്രട്ടറി മോൺ. കസഭോളി, യുഗോ സ്ളാവിയായിലെ പോസ്റ്റ് ആന്റ് ടെലഗ്രാഫ് വകുപ്പുമന്ത്രി എന്നിവ രുൾപ്പെടുന്നു.

86\. Paragraph

മി. ഡി. സെൻഗുപ്തയും മററു ആര പേരും ചേർന്നും സമപ്പിച്ച ഒരു ശ്രദ്ധതി രിക്കൽ പ്രമേയത്തിന്നും മറുപടി പറയു കയായിരുന്നു അദ്ദേഹം.

87\. Paragraph

* * * * *

88\. Paragraph

~~~~~

89\. Paragraph

എമ്പസി ആക്രമണത്തിന് അമേരിക്കൻ തിരിച്ചടി അടുത്തുണ്ടാകും.

90\. Paragraph

(റോയിട്ടർ) വാഷിംഗ്ടൺ, മാച്ച് 31

91\. Paragraph

(റോയിട്ടർ) വാഷിംഗ്ടൺ, മാച്ച് 31 സൈഗോണിലെ അമേരിക്കൻ എമ്പസിയുടെനേ രെ ഇന്നലെ ഉണ്ടായ ആക്രമണം നിഷ്ഠൂരമാ യ ഒരു നടപടിയാണെന്നും പ്രസിഡണ്ട് ജോ ൺസൺ ഇന്നലെ രാത്രി പുറപ്പെടുവിച്ച ഒരു പ്രസ്താവനയിൽ പറഞ്ഞു.

92\. Paragraph

ഇത്തരത്തിലുള്ള ആക്രമണങ്ങൾ തെ ക്കൻ വിയറ്റ്നാം ജനതക്കും ഗവണ്മേ ണ്ടിന്നും നൽകുന്ന സഹായത്തെ ശക്തി പ്പെടുത്തണമെന്നുള്ള അമേരിക്കൻ ജന തയുടേയും, ഗവണ്മെണ്ടിൻറെയും ദൃഡ നിശ്ചയത്തെ കൂടുതൽ ഉറപ്പിക്കുകയേയു ള്ളു. ഈ ആക്രമണത്തിന്നും നൽകേണ്ട തിരിച്ചടിയെ സംബന്ധിച്ച് പ്രസിഡ ണ്ടു് ജോൺസനും, അദ്ദേഹത്തിൻറെ ഉ പദേശാക്കളും മൌനം ഭജിക്കുകയാണു ഒരു തിരിച്ചടിയിൽ വടക്കൻ വിയ ററ്നാമിൻറെ ഉള്ളിലേക്ക് കടന്നുകൊ ണ്ടുള്ള ഒരു വ്യോമാക്രമണത്തെ സംബ ന്ധിച്ചു് അനൗദ്യോഗികസംസാരമുണ്ടു്. പക്ഷെ പ്രസിഡണ്ടു് പെട്ടെന്നും ഒരു

93\. Paragraph

തീരുമാനത്തിലെത്തുവാൻ ശ്രമിക്കുന്നി ല്ലെന്നുള്ളതിൻ്റെ സൂചനകളാണു് ഉള്ള തു്. തെക്കൻ വിയറ്റ്നാമിലേക്ക് ഈ തൽ അമേരിക്കൻ സേനകളെ അയക്കു മോയെന്നതും വ്യക്തമായിട്ടില്ല.

94\. Paragraph

ഒസഗോണിലെ അമേരിക്കൻ അ മ്പാസിഡർ ജനറൽ മാക്സ് വെൽടെയി ലറെ, ഇന്നോ നാളെയൊ താൻ കാണു മെന്നും പ്രസിഡണ്ടു് പത്രക്കാരോട് പ റയുകയുണ്ടായി. വിയറാ നാം സ്ഥിതി ഗതികളെ സംബന്ധിച്ചുള്ള സംഭാഷ ണത്തിനു് ടെയിലർ ഇവിടെ എത്തി യിരിക്കുകയാണ്. വടക്കൻവിയാറ് നാ മിൻറെ നേരെയുള്ളവ്യോമാമാനങ്ങൾ ശക്തിപ്പെടുത്തുന്നതിനും ടെയിലർ അ നുകൂലമാണെന്നും പറയുന്നു.

95\. Section Title

വിയറ്റ്കോങ്ങ് കേന്ദ്രം ആക്രമിച്ചു

96\. Paragraph

(റോയിട്ടർ) സൈഗോൺ മാ. 31 അമേരിക്കയുടേയും, തെക്കൻ വിയ റനാമീന്റെയും നൂറോളം വിമാനങ്ങ ൾ ഇവിടെനിന്നു 50 നാഴിക ദൂരെ കാ ട്ടിലുള്ള ഒരു വിയറ്റ്കോങ്ങ്കേന്ദ്രം ഇ ന്നും ആക്രമിച്ചു. ആക്രമണത്തിൻറ ഫലമായി ഈ കേന്ദ്രത്തിൽ തീപ്പിടി ച്ചു. വിപുലമായ നാശനഷ്ടങ്ങൾ ഉ ണ്ടായിട്ടുണ്ടു്.

97\. Paragraph

സൈഗോണിന്നും 350 നംഴിക ദൂരെ ഗറില്ലകൾ തിങ്ങികൂടിയിട്ടുള്ള ഒരു സ്ഥ ലത്തേക്ക് സൈന്യങ്ങളെ എത്തിച്ചിരു ന്ന മൂന്ന് അമേരിക്കൻ ഹെലികോപ്‌ട റകളെ കമ്യൂണിസ്റ്റ് വിയാറ്റ്കോങ്ങുക ൾ വെടിവെച്ചു. രണ്ട് അമേരിക്കൻ വൈ മാനികർ കൊല്ലപ്പെട്ടിട്ടുണ്ടു്. കൂടുതൽ വിവരങ്ങൾ അറിഞ്ഞിട്ടില്ല. ഇരുപ തോളം മററു ഹെലികോപ്‌ടറുകൾക്ക് വെടിയേറ്റിട്ടുണ്ടു്.

98\. Section Title

പ്രതികാരത്തിന്നു്

99\. Section Title

പ്രകടനം

100\. Paragraph

അമേരിക്കൻ എമ്പസിയുടെ നേരെ ഇന്നലെ ഉണ്ടായ ആക്രമണത്തിന്നു പ്ര തികാരം ചെയ്യണമെന്നും ആവശ്യപ്പെ ട്ടുകൊണ്ടു് അനേകം വിയററുനാമീസുക ൾ സൈഗോൺ സിററിഹാളിന്നു പുറ

101\. Paragraph

എമ്പസി ആക്രമണത്തിൻ്റെ ഫല മായി മരിച്ചവരുടെ സംഖ്യ ഇന്നേക്ക് 21 ആയി ഉയർന്നു. 18 വിയററ് നാമീ സുകളും രണ്ടു് അമേരിക്കക്കാരും തിരി ച്ചറിയപ്പെടാത്ത ഒരു വിദേശിയുമാണു മരിച്ചതു്. മൂന്നു് അമേരിക്കക്കാരുടെ പരിക്കുകൾ ഗുരുതരമാണെന്നു് ഒരു അമേരിക്കൻ വക്താവ് പറഞ്ഞു.

102\. Paragraph

സൌത്തിന്ത്യൻ ബാങ്കി ൻ്റെ ഇഷ്യൂവറായ

103\. Section Title

ഉൽഘാടനം ചെയ്യപ്പെട്ടു

104\. Paragraph

(സ്വ. പ്ര.) തൃശൂർ മാ. 31 തൃശൂർ ആസ്ഥാനമാക്കി പ്രവർത്തിക്കു ന്ന സൌത്തിന്ത്യൻ ബാങ്കിന്റെ ഒരു ശാഖ ഈറോഡിലുള്ള നേതാജി റോ ഡിൽ ഇന്ന് ഉൽഘാടനം ചെയ്യപ്പെട്ടി രിക്കുന്നു.

105\. Paragraph

ബാങ്കിൻ്റെ 63-ാമത്തെ ശാഖയാ ണിതു്.

106\. Headline

ഏപ്രിൽ 10-ാംനു മുതൽ കേരളത്തിലെ എല്ലാ പ്രമുഖ കേന്ദ്രങ്ങളിലും

107\. Paragraph

ഇണപ്രാവുകൾ

108\. Image

ഈ ചിത്രം ഒരു പഴയ പത്രത്തിൽ നിന്നോ പുസ്തകത്തിൽ നിന്നോ സ്കാൻ ചെയ്ത ഒരു പേജാണെന്ന് തോന്നുന്നു. ഇതിൽ ഒരു വ്യക്തിയുടെ ചിത്രം കാണാം. ചിത്രത്തിന്റെ ഗുണനിലവാരം കുറവാണ്, ഇത് ഒരു പഴയ ഫോട്ടോയോ അല്ലെങ്കിൽ ഒരു പഴയ പ്രിന്റിന്റെ പുനർനിർമ്മാണമോ ആകാം. ചിത്രത്തിൽ വ്യക്തമായ വാചകങ്ങളോ, ലേബലുകളോ, തിരിച്ചറിയാൻ കഴിയുന്ന മറ്റ് എഴുത്തുകളോ ഒന്നും കാണാനില്ല.

109\. Paragraph

ശ്രീ. മട്ടത്തുവക്കിയുടെ വിശ്രതമായ നോവൽ വെളിത്തിരയിൽ

##### Enrich visual components with text

Caption charts, images, and other visual elements

### Source document

Input

![Chemical Weekly: source document with bounding boxes](https://assets.sarvam.ai/tr:q-70,f-auto,dpr-auto/assets/products/doc-agents/samples/chemical-1.webp)

Click a block to scroll to its text

### Akshar

Sarvam

Extracted blocks · 20 detected

1\. Header

fil 18, 1989

2\. Header

CHEMICAL WEEKLY

3\. Page No.

35

4\. Headline

CHEMARENA

5\. Headline

.L. VENKITESWARAN

6\. Headline

Methanol-based acetic acid

7\. Paragraph

The project for acetic acid from methanol continues to be the news more recently after the Central Molasses Board eeting. The status of acetic acid in India was reviewed in e CHEMICAL WEEKLY (Jan. 3, 1989) and the relevance f methanol-based acetic acid referred to in these columns. fter an initial flurry of capacity approvals two years back e question was finally the approval of technology import om British Petroleum, the party who owns it, by GNFC, e party chosen by the licensor for imparting the technol- gy as a sole licencee. The proposals reported before Gov- nment of India for import of technology at over Rs. 8 crores n foreign exchange plus about Rs. 25 crores of equipment nd catalysts for a 40,000 TPA plant which may need an over- ll investment of Rs. 90 crores. This foreign exchange cost s enormous when ethyl alcohol technology needs nil.

8\. Paragraph

It is now reported that GNFC is planning to export 50% f production to their collaborator and argue that the quan- ty of 18,000 tonnes of acetic acid (at 90% capacity utili-

9\. Paragraph

sation) only will hit the Indian market and therefore will have hardly any repercussion on the production from ethyl alco- hol or on molasses utilisation. Earlier there was a report that GNFC was planning doubling of capacity with 50% exports in which case 36,000 tonnes will be for Indian market. What- ever be the quantity for Indian market it is more important to see the price at which it would be sold. Earlier estimates of costs was over Rs. 11.50 per kg. on 40,000 tonnes pro- duction. If half were exported at a price of even Rs. 8 per kg, the Indian price will go up to Rs. 15.00 per kg. -- far higher than the costs from ethyl alcohol. The attempts to jus- tify the project only lead to more questions on viability and the necessity for such production in the Indian context.

10\. Paragraph

There is an urgent need for clearance of more projects for acetic acid from ethyl alcohol on a priority basis and finan- cial institutions would do well to reexamine their old assess- ment of GNFC’s project and decide on financial clearance of other applications pending with them.

11\. Section Title

Fluoroaromatics

12\. Paragraph

Fluoroaromatics particularly derivatives of trifluoromethyl enzenene have been the base for some useful pharmaceuti- als and pesticides. More recently the fluoroquinolones which ave excellent antibiotic properties have been introduced into he market, particularly norfloxacin. Now there is a build up n fluoroaromatics to meet the increasing demands. Mallin- croft Chemicals and DuPont have been the producers in USA nd are said to be doubling their capacities. ICI in UK is also a major producer with Hoechst and Rhone Poulenc in Europe. One estimate is that the world demand is about 4,000 tonnes nd expected to grow at a high rate.

13\. Paragraph

The chlorofluoromethanes or CFC’s have had a notorious reputation in promoting ozone destruction in the stratosphere and indirectly promoting ultra violet radiation penetration and warming up of atmosphere which could have disastrous con- sequences. Fluoroplastics Teflon for example, have been very important but CFC’s and Teflon are based on simple ali- phatic molecules while the bioactive compounds are aro- matic or other ring compounds with fluorine as a substituent in the form of trifluoromethyl radical. There is a fluoroaro- matic resin however -- PEEK-based on diflurobenzophenone. Some of the fluoropesticides are of an earlier era and most

14\. Paragraph

are active herbicides. A few are still used in large volumes particularly, trifluoranil. The important products of this group of herbicides are indicated below:

15\. Paragraph

Trifluoranil (Treflan)

16\. Image

The image displays the skeletal chemical structure of a substituted benzene ring. The central hexagon represents the benzene ring, which is substituted at three positions. At the top position, a nitro group (NO₂) is attached. At the bottom position, another nitro group (NO₂) is attached. On the left side of the ring, a carbon atom is bonded to a trifluoromethyl group (F₃C). On the right side, a nitrogen atom is bonded to a group represented as N(C₃H₇)₂, indicating a nitrogen atom attached to a propyl group (C₃H₇). The structure is a symmetric derivative of 1,3-dinitrobenzene.

17\. Paragraph

Benfluoranil

18\. Image

The image displays a chemical structure diagram of a substituted benzene ring, specifically a nitroso-derivative. The central feature is a benzene ring (hexagon with a circle in the center). Attached to the ring are four substituents: a nitro group (NO₂) at the top position, a trifluoromethyl group (F₃C) at the left position, a nitrogen atom (N) at the bottom position, and a branched alkyl group on the right. This right-side group is a secondary amine, branching into two alkyl chains: an ethyl group (C₂H₅) and a butyl group (C₄H₉(n)). The structure represents a complex organic molecule, likely a precursor or intermediate in organic synthesis.

19\. Paragraph

Norfluorazon

20\. Image

The image displays a skeletal chemical structure diagram rather than a data chart with axes. The central core is a six-membered ring containing two Nitrogen (N) atoms and four Carbon (C) atoms. The ring is substituted as follows: a phenyl group (benzene ring) is attached to one Nitrogen atom; a carbon-carbon double bond (N=CH) connects the second Nitrogen to a carbon atom; and the remaining carbon atoms are substituted with a methyl group (-NHCH3) and a chlorine atom (Cl). Additionally, a trifluoromethyl group (F3C) is attached to one of the outer Carbon atoms. The structure represents a chlorinated, fluorinated heterocyclic compound, specifically a 1-phenyl-2-(trifluoromethyl)-4-chloropyridazine derivative.

##### Agent Orchestration: Plan → Reason → Act

The best document intelligence models work well on the majority of documents - achieving up to 90-95% accuracy. In domains such as healthcare, finance, government, among others, 100% is critical to aid important decision-making. Such real-world complexities can break even the most sophisticated systems.

Akshar represents a paradigm shift - from passive extraction to that of semantic understanding and contextual reasoning. By harnessing multimodal LLMs, the platform functions as a cohesive intelligence layer that reads, interprets, and executes complex flows.

##### How Agents Work

  1. Baseline Extraction: Documents are processed through Sarvam Vision’s harness modules and VLM for extractions. Agents identify, fix common errors.
  2. Agent Capabilities:
     1. Digitization: At upload time, any user-provided instructions for a document are executed autonomously across each page.
     2. Proofreading: Human-in-the-loop is now easier. Using the chat interface, interact with the agent to fix issues across pages or in select blocks.
  3. Actions and Memory: Agent performs tasks and updates memory for future recall.



All agent actions are proposed as reviewable suggestions for users to accept or reject, putting human trust and auditability front and center.

##### **Industry Extensions**

Akshar’s capabilities extend across various document types and domains:

Categories

HealthcareFinancial ServicesEducationInsuranceLegal

Health CheckupBlood TestGeneral PrescriptionDental Prescription

![Health Checkup: source document](https://assets.sarvam.ai/tr:q-70,f-auto,dpr-auto/assets/products/doc-agents/samples/medical-report-1.webp)

Extracted blocks · 9 detected

1\. Header

This image contains no text. It is a graphic icon depicting two blue legs with red heads, likely representing people or pedestrians crossing at an intersection (a zebra crossing).

2\. Section Title

Sugam Hospitals

3\. Paragraph

Symbol of Health

4\. Header

PATIENT SAFETY & QUALITY OF CARE NABH CERTIFIED

5\. Paragraph

Name : Mr.MURALI.G

6\. Table

|   
---|---  
HAEMATOLOGY - Hb | 13.9 |  |  |   
PCV | 45.6 |  |  | 44.0  
TOTAL WBC COUNT | 8570 | 6660 | 11900 | 9620  
PLATELET COUNT | 2.85 |  | 2.80 | 2.18  
DIFFERENTIAL COUNT - N | 78.9 |  |  |   
M | 5.2 |  |  |   
L | 14.1 |  |  |   
E | 1.6 |  |  |   
ESR - 1/2 Hour | 2 |  |  |   
1 Hour | 4 |  |  |   
GLUCOSE PROFILE - RBS | 345 |  |  |   
FBS |  |  |  | 173  
PPBS |  |  |  | 260  
HBA1C |  |  |  | 9.5  
RFT - UREA | 25 |  |  |   
CREATININE | 1.0 |  |  | 26  
ELECTROLYTES - SODIUM | 139 | 140 | 143 | 1.0  
POTASSIUM | 4.0 | A.4 | 3.9 |   
CHLORIDE | 100 |  |  |   
BICARBONATE | 23. |  |  |   
LIPID PROFILE |  |  |  |   
TOTAL CHOLESTEROL | 225 |  |  |   
TGL | 78 |  |  |   
HDL | 57 |  |  |   
LDL | 152 |  |  |   
VLDL | 16 |  |  |   
RF | 3.9 |  |  |   
THYROID PROFILE - FREE T3 | 2.18 | (2.0-4.4) |  |   
FREE T4 | 1.38 | (0.93-1.7) |  |   
TSH | 1.137 | (0.35-5.50) |  |   
PANCREATIC PROFILE |  |  |  |   
SERUM AMYLASE |  |  |  |   
SERUM LIPASE |  |  |  |   
LFT - BILIRUBIN - TOTAL |  |  |  |   
DIRECT |  |  |  |   
INDIRECT |  |  |  |   
SGOT |  |  |  |   
  
7\. Footer

Basysr

8\. Page No.

੨

9\. Page No.

5

##### **Conclusion**

By vertically integrating Sarvam Vision, Akshar aims to minimize friction between model capabilities and real-world applications. It harnesses isolated OCR problems with a comprehensive intelligence layer which orchestrates complex tasks. This approach addresses the reliability deficit inherent in modern AI systems due to their probabilistic nature, allowing us to unlock value trapped in unstructured documents.

### **Try it!**

Akshar is built for real-world document workflows-and we’re just getting started. To kick things off, we’re making Akshar **available in Preview at**[![](https://www.google.com/s2/favicons?domain=akshar.sarvam.ai&sz=32) akshar.sarvam.ai](https://akshar.sarvam.ai/), completely free for the month of February.

This is your chance to try it with documents of any kind, explore a wide range of use-cases, and traverse the last mile of accuracy. Every user gets **free credits** to upload documents, try Agent Mode, and experience Akshar’s capabilities end-to-end.

If you’re an individual or organization interested in using Akshar in production, we encourage you to **join our waitlist from within the platform**. You can also try Akshar via our [![](https://www.google.com/s2/favicons?domain=docs.sarvam.ai&sz=32)Document Intelligence APIs ](https://docs.sarvam.ai/api-reference-docs/document-intelligence/initialise)and experience **Sarvam Vision** on our [![](https://www.google.com/s2/favicons?domain=dashboard.sarvam.ai&sz=32)playground](https://dashboard.sarvam.ai/vision).

Curious what else we're building? Explore our APIs and start creating. 

Curious what else we're building?

Explore our APIs and start creating.

[Get Started](https://indus.sarvam.ai)
