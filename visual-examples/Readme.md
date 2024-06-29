# Case study from the online evaluation
In addition to the case displayed in the paper (Figure 3), we provide several additional examples of how the original and proposed methods differ from each other. The examples are grouped into three clusters: easy cases, hard cases, and cases containing dislikes.

- In easy cases, we have ample feedback on relatively popular items, therefore the results of both the original method and the proposed modification are practically identical.
  
- In hard cases, either
  - we have very few feedback records or are tasked to rank a long-tail category (`hard-2.png`, `hard-4.png`), or
  - we are looking for complementary products (cross-category recommendation; `hard-1.png`, `hard-3.png`).

  In such cases, the original method might be unable to provide a sufficient volume of recommendations, and we have to extend the results using a non-personalized approach. The modified approach is better at identifying relevant items in these cases. See also Figure 3 in the paper.
  
- In dislike cases, the original method often amplifies the scores of items very similar to the disliked one. In contrast, this behavior was not observed for the proposed modifications. See also Figure 1 in the paper.
