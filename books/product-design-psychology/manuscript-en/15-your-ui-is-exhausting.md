## Chapter 15 · Your UI Is Exhausting

*Why every extra thing on screen costs the user something*

![](../assets/chapter-15.png)

Nothing is obviously broken, and people still give up. That is what cognitive load looks like in products. One label needs a second read. One step is one step too many. One control asks for a small guess. None of it looks fatal in isolation, but together it drains people. By the time they reach the part that matters, they are already tired.

### The task already uses part of the budget

For years, designers repeated the number seven. [George Miller](https://psychclassics.yorku.ca/Miller/) gave them that opening, and the field turned it into a rule. [Nelson Cowan](https://psych.colorado.edu/~cowan/papers/cowan2001b.pdf) came back later and put the real number closer to four chunks held in mind at once. That matters because a lot of interfaces spend those slots before the task even starts.

[John Sweller](https://andymatuschak.org/files/papers/Sweller%20-%201988%20-%20Cognitive%20load%20during%20problem%20solving.pdf) makes the distinction that matters most here. Some effort belongs to the task. Some effort helps the user learn. Then there is the extra load the interface adds for no good reason: unclear wording, bad hierarchy, or a step that stayed because nobody wanted to remove it. That is the tax.

[Steve Krug](https://www.sensible.com/dmmt.html) put the practical version well: “Every question mark adds to our cognitive workload, distracting our attention from the task at hand.” That is the point here. It is not only about too many options. It is about the general drag created by small uncertainties.

[Fred Paas, Alexander Renkl, and John Sweller](https://doi.org/10.1207/S15326985EP3801_1) pushed the same idea further: not all load is equal. Some of it helps learning. Some of it just burns capacity. That is the distinction designers miss when they say a task is supposed to be hard. The difficulty should belong to the task, not to your wording, your structure, or your lazy defaults.

### TurboTax cut the extra work

[TurboTax](https://en.wikipedia.org/wiki/TurboTax) is useful because the underlying task is awful. Filing taxes is hard. Design cannot make the tax code simple. But TurboTax cut the extra work around the task. One question per screen. Plain English where jargon could be cut. A clear path through the process.

That is what makes the example useful. It did not remove difficulty from the problem itself. It removed difficulty from the interface wrapped around the problem. Competing products often made people hold more in mind at once, jump between sections, or decode terms they should never have had to decode.

It is worth keeping one thing clear. Intuit’s wider behavior does not make the design point false. The lesson is narrower. If the task is already heavy, the interface does not get to make it heavier.

That is what good reduction looks like. It is not pretending the task is simple. It is refusing to add extra strain around it: one clean question, one clear next step, and one less thing to remember while doing something people already dread.

That difference matters because designers often defend heavy screens by pointing to the complexity of the domain. Healthcare is complex. Finance is complex. B2B operations are complex. But that does not excuse a screen that makes users decode your internal language, remember hidden dependencies, or guess what will happen after they click.

### It is broader than choice

A screen can be exhausting with only three buttons on it if the wording is vague, the hierarchy is muddy, and the path asks the user to keep too much in mind at once. That is why designers miss it. They look for dramatic failure. What they built is often just tiring.

I have seen products lose people not because the decision was hard, but because the interface kept asking for one more little act of interpretation.

### Run the load audit

Pull up the screen people use most and count the things they have to hold in mind before they can move. Not just choices. Interpretations. Terms. Steps. Dependencies. Little moments where the user has to stop and work out what you meant. Then ask one question: does this effort help them do the task, or is it just there because the interface is making them work for your convenience?

If it is the second kind, cut it.

If you cannot cut it, move it later. A lot of exhausting screens are not overloaded because they contain too much forever. They are overloaded because they contain too much too early. Put the essential thing first and let the extra detail show up only when the user has earned the need for it. A tired user should not have to do all the sorting before they can do one useful thing.

This is where progressive disclosure actually earns its keep. Not as a pattern-library phrase, but as a way to stop spending the user’s attention before the main job is even clear. The question is simple: what does this person need to act right now, and what can wait thirty seconds?

If you spend all the attention up front, the rest of the flow is working with scraps.

Users do not always quit because they are blocked. A lot of them quit because you made the whole thing too tiring to continue.

### References & Sources

- **Sweller, J. (1988). Cognitive load during problem solving: Effects on learning.** Cognitive Science, 12(2), 257–285. [https://andymatuschak.org/files/papers/Sweller%20-%201988%20-%20Cognitive%20load%20during%20problem%20solving.pdf](https://andymatuschak.org/files/papers/Sweller%20-%201988%20-%20Cognitive%20load%20during%20problem%20solving.pdf)
- **Cowan, N. (2001). The magical number 4 in short-term memory: A reconsideration of mental storage capacity.** Behavioral and Brain Sciences, 24(1), 87–114. [https://psych.colorado.edu/~cowan/papers/cowan2001b.pdf](https://psych.colorado.edu/~cowan/papers/cowan2001b.pdf)
- **Paas, F., Renkl, A., & Sweller, J. (2003). Cognitive load theory and instructional design: Recent developments.** Educational Psychologist, 38(1), 1–4. [https://doi.org/10.1207/S15326985EP3801_1](https://doi.org/10.1207/S15326985EP3801_1)
- **Wikipedia: Cognitive load.** [https://en.wikipedia.org/wiki/Cognitive_load](https://en.wikipedia.org/wiki/Cognitive_load)
- **Krug, S. (2000). Don't Make Me Think: A Common Sense Approach to Web Usability.** New Riders Press. [https://www.sensible.com/dmmt.html](https://www.sensible.com/dmmt.html)
- **Nielsen Norman Group: Minimize Cognitive Load to Maximize Usability.** [https://www.nngroup.com/articles/minimize-cognitive-load/](https://www.nngroup.com/articles/minimize-cognitive-load/)
- **Interaction Design Foundation: Cognitive Load Theory.** [https://www.interaction-design.org/literature/topics/cognitive-load](https://www.interaction-design.org/literature/topics/cognitive-load)
