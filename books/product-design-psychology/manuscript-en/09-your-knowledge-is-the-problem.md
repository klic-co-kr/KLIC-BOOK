## Chapter 9 · Your Knowledge Is the Problem

*Why experts judge their own work worst*

![](../assets/chapter-09.png)

When you review your own design, you are not seeing what a first-time user sees. The version in front of you, the one you have stared at for weeks, gets covered up in your head by everything you know about it. The button that does the thing you built? You already know what it does. Your eyes land on it and the meaning shows up before you have even read it properly. At that point, you are not really reading the interface anymore. You are reading your memory of making it. A beginner lands on that same screen with none of that context. They read the button, or try to. They might not even know it is clickable.

I have watched that happen on screens I thought were painfully clear.

### What your context hides

In 1989, economists [Colin Camerer, George Loewenstein, and Martin Weber](https://www.cmu.edu/dietrich/sds/docs/loewenstein/CurseknowledgeEconSet.pdf) ran a set of experiments at Wharton. The question was simple: can people who know something predict what it looks like to people who do not? They cannot. Give someone information and ask them to imagine not having it. They fail, every time. And the more they know, the worse they get. Camerer’s team called this the *curse of knowledge*. Once that understanding is in your head, you do not just carry it around. It starts getting in the way of what you see.

The problem is memory, not personality. Looking at something familiar, your brain does not stop and inspect it carefully. It rebuilds it fast, below awareness. So the screen you designed does not look fresh to you anymore. It looks complete. The vague label feels clear enough. The tucked-away feature hardly looks hidden. You fill the whole thing in with context the user never had.

[Carl Wieman](https://www.aps.org/publications/apsnews/200711/backpage.cfm) spent years studying this in university physics. His finding was blunt: “when you know something, it is extremely difficult to think about it from the perspective of someone who does not know it.” Wieman was talking about professors who could not understand why students struggled with concepts they found obvious. He could just as easily have been describing a designer watching a test and thinking: how did they not see that?

> *When you know something, it is extremely difficult to think about it from the perspective of someone who doesn’t.*
> — Carl Wieman

### Photoshop was built for experts

Photoshop grew out of professional image-making workflows. Adobe’s own history notes that John Knoll was working at Industrial Light & Magic while the software was taking shape, and Adobe says Photoshop’s primary user base has long been professional designers and photographers. That context matters. Masking, adjustment layers, blend modes: these were not beginner concepts. They were basic vocabulary. In the same way a carpenter does not stop to explain what a chisel is for, the people shaping Photoshop did not really feel what the interface was asking beginners to understand. ([Adobe on Photoshop’s origins](https://blog.adobe.com/en/publish/2015/02/18/photoshop-turns-25-qa-with-thomas-knoll), [Adobe on Photoshop’s core audience](https://blog.adobe.com/en/publish/2015/02/25/adobe-explains-it-all-photoshop))

First-time users had to wrestle with it. Even Adobe’s own beginner materials have to stop and teach the concepts experts take for granted, especially layers. Which layer am I on? Why is this edit not applying? What is the difference between these two brushes? The people building the tool could not feel those as problems anymore. [Nielsen Norman Group’s research on cognitive walkthroughs](https://www.nngroup.com/articles/cognitive-walkthroughs/) documents exactly this:

> *Structured evaluations simulating a first-time user exist specifically because designers are not capable of generating that experience on their own. The knowledge blocks it.*

Adobe eventually shipped Lightroom. Then Photoshop Elements, which Adobe now describes as “smart, easy-to-use photo editing software” for “anyone” with “no experience needed.” The people who built Photoshop could not make Photoshop feel clear to beginners just by polishing the same product again. They had to build something else. ([Adobe Photoshop Elements](https://www.adobe.com/products/photoshop-elements.html))

### The beginner was not in the room

In real teams, it usually goes like this. Designers review the flow and find it obvious. A developer reads the error message and it seems clear enough. The PM sits through the onboarding demo and no one questions it. Everyone nods. Then a first-time user hits “Continue” and has no idea what the button is about to do.

Then users show up. They stop at the step everyone thought was easy. They ignore the feature that took weeks to build. They go sideways at the moment the path was supposed to be straight. And because the room already has all the context, people watch this happen and still sound surprised.

The post-mortem keeps landing on the same thing. The group assumed users would arrive with context that only existed inside the team. I have seen that happen after launches that looked completely fine in review.

Awareness does not fix this. [Camerer’s research](https://www.cmu.edu/dietrich/sds/docs/loewenstein/CurseknowledgeEconSet.pdf) found that informing people about the curse had almost no effect on how much it affected their judgment. You can read about it, understand it, explain it to someone else, and still miss the holes in your own work. I still catch myself doing that on tired Fridays. Knowing the bias exists and seeing past it are two different jobs.

### Put a new person in front of it

What works best is external. Find someone who has genuinely never seen the thing. Not a colleague who was in the kickoff. Not a designer from another team who heard you mention it in passing. Bring in someone with no context at all. Put the product in front of them. Watch, stay quiet, let them react, and let the silence sit. Pay attention to where they slow down, misread, or give up.

Each of those moments marks a gap your own knowledge had been filling. The [curse of knowledge](https://en.wikipedia.org/wiki/Curse_of_knowledge) is not something you can think your way out of. [Chip and Dan Heath put it plainly in Harvard Business Review](https://hbr.org/2006/12/the-curse-of-knowledge): they called it the biggest single obstacle between a designer and the people they design for. The same expertise that helped make the thing also gets in the way. I have seen designers keep polishing the same screen while missing the fact that fresh people could not read it at all.

What matters is not what you made. It is what a fresh person sees.

### References & Sources

- **Camerer, C., Loewenstein, G., & Weber, M. (1989). The curse of knowledge in economic settings: An experimental analysis.** Journal of Political Economy, 97(5), 1232–1254. [https://www.cmu.edu/dietrich/sds/docs/loewenstein/CurseknowledgeEconSet.pdf](https://www.cmu.edu/dietrich/sds/docs/loewenstein/CurseknowledgeEconSet.pdf)
- **Heath, C., & Heath, D. (2006). The curse of knowledge.** Harvard Business Review, 84(12), 20–23. [https://hbr.org/2006/12/the-curse-of-knowledge](https://hbr.org/2006/12/the-curse-of-knowledge)
- **Wieman, C. E. (2007). The "curse of knowledge," or why intuition about teaching often fails.** APS News, 16(10). [https://www.aps.org/publications/apsnews/200711/backpage.cfm](https://www.aps.org/publications/apsnews/200711/backpage.cfm)
- **Wikipedia: Curse of knowledge.** [https://en.wikipedia.org/wiki/Curse_of_knowledge](https://en.wikipedia.org/wiki/Curse_of_knowledge)
- **The Decision Lab: Curse of Knowledge.** [https://thedecisionlab.com/reference-guide/management/curse-of-knowledge](https://thedecisionlab.com/reference-guide/management/curse-of-knowledge)
- **Nielsen Norman Group: Evaluate Interface Learnability with Cognitive Walkthroughs.** [https://www.nngroup.com/articles/cognitive-walkthroughs/](https://www.nngroup.com/articles/cognitive-walkthroughs/)
- **Adobe Blog (2015). Dreams from the Digital Darkroom: 25 Years of Photoshop.** [https://blog.adobe.com/en/publish/2015/02/18/photoshop-turns-25-qa-with-thomas-knoll](https://blog.adobe.com/en/publish/2015/02/18/photoshop-turns-25-qa-with-thomas-knoll)
- **Adobe Blog (2015). Adobe Explains It All: Photoshop.** [https://blog.adobe.com/en/publish/2015/02/25/adobe-explains-it-all-photoshop](https://blog.adobe.com/en/publish/2015/02/25/adobe-explains-it-all-photoshop)
- **Adobe. Photoshop Elements 2026.** [https://www.adobe.com/products/photoshop-elements.html](https://www.adobe.com/products/photoshop-elements.html)
