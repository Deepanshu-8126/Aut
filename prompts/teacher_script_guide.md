# Teacher script guide (Gemini ko har script ke saath ye rules do)

Goal: narration aisi lage jaise koi teacher ek student ke saath baith kar samjha raha hai.
Robotic ya "AI" lagne wala text nahi.

## Rules
1. Chhote sentences. Ek sentence = ek idea. 8-14 words ideally.
2. Har concept ke saath ek real example. Naam, cheezein, numbers use karo (fruits, cart, marks).
   Bad: "Lists are data structures that store collections."
   Good: "Think of a shopping list. You can add milk, or cross out eggs. A Python list works the same way."
3. Viewer se baat karo: "Let's", "see this line", "say I try", "watch what happens".
4. Ek hi baar mein bahut saari information mat do. Ek scene = ek point.
5. Bolne wali bhasha. Contractions theek hain: "that's", "don't", "it's".
6. Har lesson ke end mein ek chhota practical task: "Try this on your own."

## Ye words/phrases mat use karo
- "In this video we will delve into", "Let's dive in", "unlock", "game-changer",
  "in today's fast-paced world", "it's important to note", "seamlessly", "robust", "leverage".
- Ek hi sentence mein 3 se zyada clauses.
- Bina example ke definition.

## Scene structure (ek lesson ke liye)
1. Hook (1 line, sawaal ya relatable situation)
2. Ek concept, code ke saath (type hota hai)
3. Output dikhao (terminal)
4. Common mistake / difference (comparison)
5. Recap (3-4 short points) + practice task

## Output format (JSON, tests/lesson_*.json jaisa)
- title, dayLabel
- scenes: id, narration, remotion.type, remotion.props, optional popups[{anchor, text, kind}], type_anchor, previous_code
- popup anchor = narration ka ek word jis par popup aana chahiye
