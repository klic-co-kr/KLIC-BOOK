## Chapter 29 · Users Will Ignore You

*Why users ignore most of what you build*

![](../assets/chapter-29.png)

You built something you care about. You worked on the layout, rewrote the copy, and kept adjusting the details. Then the user opened it, glanced for two seconds, and moved on, not because your work was bad, but because they already had too many other things competing for their attention.

That is the bad assumption under a lot of product work: users show up ready to engage. They do not. By the time someone reaches your product, their attention has already been spent somewhere else. A hard email. A Slack message. A call that ran long. Something half-finished. What you get is whatever is left. Some days, not much.

### Attention is limited

[Herbert Simon](https://www.press.jhu.edu/) wrote about this in 1971, long before the internet made it feel urgent. He was looking at information abundance and landed on something that still holds:

> *A wealth of information creates a poverty of attention and a need to allocate that attention efficiently among the overabundance of information sources.*
> — Herbert Simon

Information does not enter the mind for free. Every piece of it needs processing. Processing costs attention. And attention, unlike the information competing for it, does not scale. You can flood someone with content. You cannot give them more capacity to take it in.

[Daniel Kahneman’s](https://books.google.com/books?id=hAkFAAAAMAAJ) 1973 work on attention showed that attention is not a spotlight you aim wherever you want. It is a budget. A limited one. The filtering starts early. Most things never get through. You do not notice what you ignored because ignoring it is the point.

This is why banner blindness is real and does not go away because you redesigned the banner. Users learn that certain positions on a page mean noise. Once that link forms, the brain skips those areas by reflex, even when they later hold something useful. [Nielsen Norman Group](https://www.nngroup.com/articles/banner-blindness-old-and-new-findings/) has tracked this for years in eye-tracking studies: once a pattern gets tagged as noise, the content inside it stops registering.

### Split attention weakens every message

[David Strayer and William Johnston](https://pubmed.ncbi.nlm.nih.gov/11760132/) put drivers in a simulator in 2001 and had them hold phone conversations while driving. Handheld phone: worse performance. Hands-free phone: same result. The hand was not the problem. The conversation was. Drivers on cell phones missed more than twice as many simulated traffic signals as undistracted drivers. Their eyes were on the road. Their attention was not. Strayer and Johnston called it inattentional blindness: you can look right at something and still miss it because seeing takes more than open eyes.

That is who opens your product. Not a blank-slate person with a clear schedule and a quiet mind. Someone mid-thought. Mid-task. Already partly somewhere else before your screen loaded.

An interface that demands focus is usually losing before it starts. A notification that interrupts is drawing from a budget the user never agreed to share with you. A modal that fires three seconds in is betting that this exact moment is the right moment, for this person, with whatever scraps of attention showed up today. That is usually a bad bet.

### Facebook measured the problem

In 2018, [Facebook rewrote its News Feed algorithm](https://www.wsj.com/articles/the-facebook-files-11631713039). Documents leaked by whistleblower [Frances Haugen](https://en.wikipedia.org/wiki/Frances_Haugen) and published by the Wall Street Journal in 2021 told a plain story. The revised algorithm optimized for emotional reactions, the kind that get comments, shares, and heated replies. The content producing the most of those signals was content that made people angry. Internal memos recorded that harmful content was “inordinately prevalent among reshares.”

What the algorithm had done was find a reliable way to hold attention. Outrage keeps people engaged in a way calmer content often does not. But that attention still comes from somewhere. Every extra minute Facebook held came out of something else: sleep, rest, conversation, work, or whatever else the person meant to be doing. Facebook understood attention well enough to exploit the mechanism. It did not treat attention as finite and worth protecting, and that problem later showed up in a Congressional hearing.

### The lesson is not to make your product louder

Before any notification goes out, before any modal launches, before any badge gets added to a tab, ask one question: what was this person doing before this moment, and is this worth interrupting them for? If you cannot answer the first part, you are designing for someone who has no life outside your product. That is not the person most products are meeting.

When someone skips past something you built, the answer is not to make it bigger. Bigger often teaches people to filter you out faster. I have seen teams add brighter colors and louder badges only to make the thing easier to ignore next time.

Ask whether it deserved the interruption at all. Cut it if it did not.

Users do not ignore your product because they do not care. They ignore it because skipping a badge, a modal, or a push alert is how they get through the day.

### References & Sources

- **Kahneman, D. (1973). Attention and Effort.** Prentice-Hall. [https://books.google.com/books?id=hAkFAAAAMAAJ](https://books.google.com/books?id=hAkFAAAAMAAJ)
- **Strayer, D. L., & Johnston, W. A. (2001). Driven to distraction: Dual-task studies of simulated driving and conversing on a cellular telephone.** Psychological Science, 12(6), 462–466. [https://pubmed.ncbi.nlm.nih.gov/11760132/](https://pubmed.ncbi.nlm.nih.gov/11760132/)
- **Simon, H. A. (1971). Designing organizations for an information-rich world.** In M. Greenberger (Ed.), Computers, Communication, and the Public Interest. Johns Hopkins Press.
- **Wikipedia: Attention economy.** [https://en.wikipedia.org/wiki/Attention_economy](https://en.wikipedia.org/wiki/Attention_economy)
- **Wikipedia: Inattentional blindness.** [https://en.wikipedia.org/wiki/Inattentional_blindness](https://en.wikipedia.org/wiki/Inattentional_blindness)
- **Nielsen Norman Group: Banner Blindness: Old and New Findings.** [https://www.nngroup.com/articles/banner-blindness-old-and-new-findings/](https://www.nngroup.com/articles/banner-blindness-old-and-new-findings/)
- **Horwitz, J. (2021). The Facebook Files.** Wall Street Journal. [https://www.wsj.com/articles/the-facebook-files-11631713039](https://www.wsj.com/articles/the-facebook-files-11631713039)
