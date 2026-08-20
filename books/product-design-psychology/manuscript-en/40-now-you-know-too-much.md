## Chapter 40 · Now You Know Too Much

*The ethics of designing with psychological knowledge*

![](../assets/chapter-40.png)

You got into design because you wanted to make things people could use without second-guessing. You cared about the craft, where something goes, why a choice feels right, how a small change can make a task easier to finish.

Now you know more than that. You know how defaults steer people, how friction changes behavior, how pressure, habit, and framing shape decisions. That knowledge makes you better at the work. It also lets you push people somewhere they would not have chosen on clear terms.

Once you know that, you do not get to pretend design is neutral.

### This knowledge was never neutral

[B. J. Fogg](https://www.sciencedirect.com/book/9781558606432/persuasive-technology) spent years mapping out how technology changes what people think and do. He coined the word “captology” for it, computers as persuasive technologies. His 2003 book ends with a question that still lands:

> *Who will wield this power of digital influence? And to what end?*
> — B. J. Fogg

Fogg asked that as an invitation to sit with it. The tools spread faster than the reflection did. Defaults, framing, loss aversion, goal gradients, cognitive load, social proof, all of it gets used every day in products people rely on. Some choices help people do what they came to do. Some push them somewhere else.

What you know about defaults lets you turn an opt-in into an opt-out. Understanding loss aversion helps you design a reassuring undo button, or a cancellation flow that makes leaving feel costly. Knowing that people are more motivated when they feel almost done helps you build a progress bar that keeps a real task moving, or fake momentum that pulls one more action from a user before they stop to think. The psychology is identical. The direction is a choice.

### What the industry shipped

In 2018, [GDPR](https://en.wikipedia.org/wiki/General_Data_Protection_Regulation) came into force across Europe. Websites needed real consent before collecting personal data. The law was specific: consent had to be informed, given without coercion, and as easy to withdraw as to give.

Researchers at Aarhus University and MIT ([Nouwens, Liccardi, Veale, Karger, & Kagal, 2020](https://arxiv.org/abs/2001.02479)) scraped the designs of the five most popular consent management platforms across the top 10,000 websites in the UK. Only 11.8% of those sites met the minimal legal requirements for consent. The rest used dark patterns that directed users toward accepting cookies through friction, framing, and missing options. In a follow-up experiment with 40 participants, the researchers showed that removing the opt-out button from the first screen increased cookie acceptance by 22 to 23 percentage points.

The message did not change. The no just got harder to find. The result was predictable: more acceptance, less informed choice. A pattern does not become acceptable because it is common. This was widespread in the sample, not an edge case.

### The line is hard to draw

There is no clean boundary where persuasion becomes manipulation. That is what makes this hard. A progress bar that helps someone finish a real task is good design. A progress bar that manufactures urgency around a fake deadline is a dark pattern. The difference is not in the component. It sits in the intent behind it and the accuracy of what it communicates. Is this indicator reflecting something true? Or is it built to push behavior whether the user wants it or not?

[Harry Brignull](https://archive.org/details/DarkPatterns-UxBrighon2010) named dark patterns in 2010 and spent years cataloguing them. Things like trick questions, hidden costs, guilt-tripping copy, and making it harder to leave than to sign up. The list helps. It also leaves harder cases, where the pattern is not an outright trick but still leans on confusion, pressure, or fatigue. A pre-checked consent box is obvious. A countdown timer that creates fake urgency is a little less so. An interface that makes the free plan so inconvenient that most people upgrade without fully choosing to sits somewhere else again.

You will work in that gray zone. The question is what you do there.

### Ask this before it ships

There is no checklist for this. No framework that tells you where persuasion ends and manipulation starts. Ask this before something ships: if the person using this knew exactly what I built here and why, would they feel helped or deceived?

I do not mean ordinary annoyance or friction. Those are part of the job. Design has trade-offs, and users do not have to love every decision you made. The line I care about is simpler: did the person understand what they agreed to, or did the design carry them past a choice they would have made differently if the screen had been clearer? You usually know which one you built.

That is the uncomfortable part about getting this far. You cannot claim ignorance anymore. You know what defaults do. By now you also know how friction shapes behavior. Hiding the cancel button is a choice about whose side you are on. I think that is where the job stops being neutral.

Designers have more psychological knowledge at their finger tips now than ever. Used carefully, that knowledge makes things easier and less frustrating. Used against people, it produces the kind of web most of us are tired of using.

The material in this book does one thing on its own: it shows you how much influence the job carries. Use it for the person using the product and you clear a path. Use it against them and you add to the reasons people approach interfaces with suspicion.

By now you know enough. You do not get to call the result neutral anymore.

### References & Sources

- **Fogg, B. J. (2003). Persuasive Technology: Using Computers to Change What We Think and Do.** Morgan Kaufmann / Elsevier. [https://www.sciencedirect.com/book/9781558606432/persuasive-technology](https://www.sciencedirect.com/book/9781558606432/persuasive-technology)
- **Brignull, H. (2010). Dark patterns: User interfaces designed to trick people.** Talk presented at UX Brighton, 2010. [https://archive.org/details/DarkPatterns-UxBrighon2010](https://archive.org/details/DarkPatterns-UxBrighon2010)
- **Nouwens, M., Liccardi, I., Veale, M., Karger, D., & Kagal, L. (2020). Dark patterns after the GDPR: Scraping consent pop-ups and demonstrating their influence.** CHI '20: Proceedings of the 2020 CHI Conference on Human Factors in Computing Systems. [https://arxiv.org/abs/2001.02479](https://arxiv.org/abs/2001.02479)
- **Thaler, R. H., & Sunstein, C. R. (2008). Nudge: Improving Decisions About Health, Wealth, and Happiness.** Yale University Press. [https://yalebooks.yale.edu/book/9780143115267/nudge/](https://yalebooks.yale.edu/book/9780143115267/nudge/)
- **Wikipedia: Dark pattern.** [https://en.wikipedia.org/wiki/Dark_pattern](https://en.wikipedia.org/wiki/Dark_pattern)
- **Wikipedia: Persuasive technology.** [https://en.wikipedia.org/wiki/Persuasive_technology](https://en.wikipedia.org/wiki/Persuasive_technology)
- **Nielsen Norman Group: Ethics in UX Design.** [https://www.nngroup.com/topic/ethics/](https://www.nngroup.com/topic/ethics/)
