## Chapter 19 · Fake Progress Is Real Motivation

*Why showing progress makes people push harder to finish*

![](../assets/chapter-19.png)

Most designers treat a progress bar as information. It keeps users calm during a slow load, or reassures them mid-signup that the whole thing will end. It gets added because users complained about not knowing where they were, because the design felt more transparent with it than without, or because it simply seemed polite. But that is only part of what it does.

When people see themselves moving toward a goal, they speed up, push harder, and become less willing to stop. A progress indicator does more than show where someone is. It can change what they do next. I have seen designers treat that as a neutral UI detail when it clearly is not. The component looks informational, but the effect is motivational.

### The meter changes what people do

In 1932, the behaviorist [Clark Hull](https://doi.org/10.1037/h0072640) proposed what he called the goal-gradient hypothesis: animals put in more effort as they get closer to a reward. He tested it by timing rats in a straight runway. The closer they got to food, the faster they ran. Hull saw this as a basic feature of goal-directed behavior: the nearer the goal, the more the organism accelerates.

The hypothesis sat in the animal behavior literature for decades. Then in 2006, researchers [Joseph Nunes and Xavier Drèze](http://msbfile03.usc.edu/digitalmeasures/jnunes/intellcont/Endowed%20Progress%20Effect-1.pdf) ran a field experiment at a car wash. They gave 300 customers loyalty cards. One version needed eight stamps for a free wash. The other showed ten spaces, but two were already stamped. Both groups still needed eight washes. The only difference was how the job felt. One group looked like it had already begun. The other did not. Completion for the pre-stamped card was 34 percent. For the blank one, 19 percent. The pre-stamped customers also came back faster as they got closer to the reward. The work was the same. The distance was the same. The result was not. Nunes and Drèze called this the endowed progress effect: give people a head start, even a fake one, and they work harder to finish.

The same pattern shows up in both cases. Once you feel that you are already in the task, finishing starts to matter more. Work that has not started yet is easy to drop. Work that already feels underway is harder to abandon. As the finish line gets closer, that pressure gets stronger. Effort is not steady across a goal. It rises near the end, which is why a half-filled bar changes the mood of the task even before the user has done much.

The [Nielsen Norman Group](https://www.nngroup.com/articles/progress-indicators/) found that users wait longer and feel better about it when a progress indicator is present, even when the actual wait time is identical. The bar does not change the labor itself. It changes how the user feels about it.

### LinkedIn made the task feel underway

LinkedIn built its profile completion meter in the early days of the platform’s growth. Members progressed from Beginner through Intermediate and Advanced to Expert and, at the top, All-Star. Every stage showed what you had and what was missing. LinkedIn documented that users with complete profiles were forty times more likely to receive opportunities through the platform.

But the completion meter was not just useful information. It hooked the user from the moment they registered. No one started at zero. The gauge appeared partly filled, with suggestions already flagged. You had already begun. The profile was already unfinished. I think that matters more than most designers admit. LinkedIn did not need persuasive copy about the benefits of a complete profile. It changed the state of mind users arrived in. The meter had already put them inside the task. Users did not just see progress. They felt that something was left unfinished.

### Most teams start too cold

Most designers who build progress indicators are thinking about user anxiety. They add the component because users felt lost, or because someone in a meeting said it would help completion rates, or because every other app in the category has one. They are thinking about feedback, not motivation. I have watched designers debate colors and labels for half an hour without once asking what the starting state made people feel.

So the bar starts empty. Zero percent. A blank slate. The user sees work ahead, not work already underway. That gives orientation, but it does not create momentum. Then designers wonder why people drop early even when the flow itself is short.

I have seen that exact move in product work more than once. The designer thinks they gave the user clarity. What they actually gave them was a clean picture of how much effort still sat in front of them.

[Ran Kivetz, Oleg Urminsky, and Yuhuang Zheng](https://faculty.chicagobooth.edu/oleg.urminsky/research/KivetzUrminskZheng2006.pdf) replicated and extended the Hull and Nunes findings across a series of studies on human loyalty programs. Their central finding holds across contexts: effort accelerates as a function of proportional distance remaining, not absolute distance. A user who feels close pushes harder than a user who feels like they are still at the beginning, even if the real work left is identical.

### Check how it starts

Before shipping any progress mechanism, run one check. Remove the starting state from the design and look at what remains. If the meter begins at zero with no pre-completed stage and no acknowledgment of what the user has already done, you do not really have a progress mechanism. You have a countdown. A countdown can reduce anxiety, but it does not do much to increase effort.

The question is not just whether the meter shows users where they are. Any meter can do that. The more useful question is whether it puts them inside something they feel pulled to finish. I think designers miss that because the component looks harmless.

Those are different design problems. The first is about visibility. The second is about motivation. You can solve both at the same time. Start the meter with something already filled. Acknowledge prior actions as completed steps: they clicked a link, they confirmed their email, they arrived on the page. Frame the state at entry as incomplete rather than unbegun.

A user who opens a form at step one of five, with visible movement already on the screen, is in a different state than one facing an empty checklist. The first user feels partway in. The second still feels at the start. I would not treat those as the same design problem.

A progress tracker that starts at zero is mostly a counter. The motivational part starts working when users feel like they are already on their way.

### References & Sources

- **Nunes, J. C., & Drèze, X. (2006). The endowed progress effect: How artificial advancement increases effort.** Journal of Consumer Research, 32(4), 504–512. [http://msbfile03.usc.edu/digitalmeasures/jnunes/intellcont/Endowed%20Progress%20Effect-1.pdf](http://msbfile03.usc.edu/digitalmeasures/jnunes/intellcont/Endowed%20Progress%20Effect-1.pdf)
- **Hull, C. L. (1932). The goal-gradient hypothesis and maze learning.** Psychological Review, 39(1), 25–43. [https://doi.org/10.1037/h0072640](https://doi.org/10.1037/h0072640)
- **Kivetz, R., Urminsky, O., & Zheng, Y. (2006). The goal-gradient hypothesis resurrected: Purchase acceleration, illusionary goal progress, and customer retention.** Journal of Marketing Research, 43(1), 39–58. [https://faculty.chicagobooth.edu/oleg.urminsky/research/KivetzUrminskZheng2006.pdf](https://faculty.chicagobooth.edu/oleg.urminsky/research/KivetzUrminskZheng2006.pdf)
- **Wikipedia: Goal-gradient hypothesis.** [https://en.wikipedia.org/wiki/Goal-gradient_hypothesis](https://en.wikipedia.org/wiki/Goal-gradient_hypothesis)
- **Nielsen Norman Group: Progress Indicators Make a Slow System Less Insufferable.** [https://www.nngroup.com/articles/progress-indicators/](https://www.nngroup.com/articles/progress-indicators/)
- **UX Collective: The Psychology of Progress Bars.** [https://uxdesign.cc/the-psychology-of-progress-bars-f4b2e6c19b10](https://uxdesign.cc/the-psychology-of-progress-bars-f4b2e6c19b10)
