## Chapter 12 · Your Design Is Rigged

*How defaults and framing steer behavior silently*

![](../assets/chapter-12.png)

You may think you are presenting a neutral choice, but you are not. The moment you decide which option starts checked, which plan gets emphasis in the pricing table, and which button sits on the left, you have already cast your vote. The screen starts leaning on people before they do anything.

Most designers never name this. Defaults get treated as technical details, placeholder states, or things to sort out later. But users will not be sorting anything out. A lot of the time, they will click what is already selected.

### Why defaults work

Defaults do not read like decisions to the person receiving them. A default says: this is normal, this is what most people do. Users read it as a recommendation even when you meant nothing by it.

Sometimes you just copied the setup from the last version and moved on.

[Amos Tversky and Daniel Kahneman](https://sites.stat.columbia.edu/gelman/surveys.course/TverskyKahneman1981.pdf) showed this in 1981, in research that still makes designers shift in their seat. They gave participants identical scenarios framed two different ways. “200 people will be saved” and “400 people will die” describe the same outcome. People chose differently based on how the choice sat on the page. The frame changed the decision. The facts did not. A default works as a frame too. It tells people what the normal state looks like, what the baseline is, and what it means to choose something else.

In 2003, [Eric Johnson and Daniel Goldstein](https://www.dangoldstein.com/papers/DefaultsScience.pdf) published a short paper in Science comparing organ donation rates across European countries. Countries where citizens had to opt in to become donors had rates between 4 and 28 percent. Countries where donation was the default, and opting out required active registration, had rates from 86 to nearly 100 percent. The populations were similar. The general attitude toward donation was similar too. Johnson and Goldstein found the explanation in effort: deciding takes work, accepting the default takes none. The default did not reveal what people valued so much as show which direction required action.

Three forces sit behind this behavior. People read defaults as quiet recommendations from whoever set them. Changing a preset takes effort, and most people will not spend that effort on something they are not sure about. Because of loss aversion, the current state also feels safer than the alternative, even when the options are equal. So the opening state shapes behavior far more than the copy around it.

### This happens in small choices

In the 1990s, [Microsoft](https://en.wikipedia.org/wiki/Microsoft) shipped [Internet Explorer](https://en.wikipedia.org/wiki/Internet_Explorer) on every Windows machine in the world. By 2003, IE held 95 percent of browser market share. Not because it was the best browser or because users compared options and chose it carefully. Mostly because it was there.

Changing it meant knowing alternatives existed, finding them, downloading them, and making a fresh decision. Almost no one did. When [Firefox](https://en.wikipedia.org/wiki/Firefox) launched in 2004 and [Chrome](https://en.wikipedia.org/wiki/Google_Chrome) followed in 2008, both needed serious campaigns to pull users away from the starting option Microsoft had set years earlier. What began as a browser setting had become a market advantage.

You do not need Windows to get this effect. You get it any time you start with a checked box. Any time you mark one pricing plan as “recommended.” Any time you order form fields in a way that makes one path seem more natural than the others.

I have seen designers wave this off as harmless when it clearly was not. The damage often looks small because it happens a tap at a time.

### The choice was shaped before the click

Designers tend to think about mental effort as a problem of too much information on screen. But defaults create that problem too, just in a quieter way. Every time a user faces a real choice, they spend effort reading, comparing, and deciding. A preset removes that cost. It says “here is the answer, act only if you disagree.”

For routine, low-stakes choices, that is solid design. It saves people from small decisions they do not care about.

For choices where your interests and the user’s interests pull in different directions, it becomes something else.

Marketing opt-ins that begin checked. Subscription tiers set to the most expensive plan. Privacy settings that open at maximum data sharing. Cookie consent flows where “accept all” takes a single tap and “manage preferences” opens a maze.

None of these read like big design decisions when you build them. They can look like startup settings. But every case has real consequences for a real person who may not notice they were being steered.

[Richard Thaler and Cass Sunstein](https://yalebooks.yale.edu/book/9780143115267/nudge/), in their 2008 book *Nudge*, put it plainly: every choice environment has an architecture, and architects can’t avoid building it. There is no neutral arrangement. The only question is whether you’re shaping that architecture with your eyes open or closed.

### Check the starting state

Before you ship any screen, name every default opening on it. Checked boxes, pre-filled fields, the emphasized pricing tier, the primary button, the order of items in a dropdown, the state the page opens in. For each one, ask: if a user touches nothing and just hits continue, where do they end up? Then ask: does that outcome serve them, or does it mainly serve you?

Defaults are good design when they reflect what most users want, when they save people from choices they have already made elsewhere, and when they reduce friction on a path the user wants to take. If your form asks for a country and most of your users are in Germany, defaulting to Germany is a service. I like defaults when they spare people work they never wanted.

If your settings screen opens with full data sharing enabled and buries the controls three screens deep, that is not. It is the difference between pre-filling a city field and pre-ticking a marketing box.

Every preset is a vote. You cast it when you built the screen. The user either accepts it or spends effort to override it, and most people will accept it when they are tired, distracted, or in a hurry.

The right question at every design review is not just “did we make this clear?” Ask “who does this default opening serve when no one is paying attention?” A lot of your users will not be.

### References & Sources

- **Tversky, A., & Kahneman, D. (1981). The framing of decisions and the psychology of choice.** Science, 211(4481), 453–458. [https://sites.stat.columbia.edu/gelman/surveys.course/TverskyKahneman1981.pdf](https://sites.stat.columbia.edu/gelman/surveys.course/TverskyKahneman1981.pdf)
- **Johnson, E. J., & Goldstein, D. (2003). Do defaults save lives?** Science, 302(5649), 1338–1339. [https://www.dangoldstein.com/papers/DefaultsScience.pdf](https://www.dangoldstein.com/papers/DefaultsScience.pdf)
- **Thaler, R. H., & Sunstein, C. R. (2008). Nudge: Improving Decisions About Health, Wealth, and Happiness.** Yale University Press. [https://yalebooks.yale.edu/book/9780143115267/nudge/](https://yalebooks.yale.edu/book/9780143115267/nudge/)
- **Wikipedia: Default effect (psychology).** [https://en.wikipedia.org/wiki/Default_effect_(psychology)](https://en.wikipedia.org/wiki/Default_effect_%28psychology%29)
- **Wikipedia: Choice architecture.** [https://en.wikipedia.org/wiki/Choice_architecture](https://en.wikipedia.org/wiki/Choice_architecture)
- **Nielsen Norman Group: Choice Architecture and Defaults.** [https://www.nngroup.com/articles/choice-architecture/](https://www.nngroup.com/articles/choice-architecture/)
- **The Decision Lab: Default Effect.** [https://thedecisionlab.com/biases/default-effect](https://thedecisionlab.com/biases/default-effect)
