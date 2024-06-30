## Results highlights
|               | EASE          | abs(EASE)     |  
| ------------- | ------------- | ------------- |
| recall @ 20   | 0.0251 | 0.0252 |
| nDCG @ 20     | 0.0432 | 0.0432 |
| recall @ 50   | 0.0468 | 0.0475 |
| nDCG @ 50     | 0.0618 | 0.0623 |
| recall @ 100  | 0.0710 | 0.0732 |
| nDCG @ 100    | 0.0790 | 0.0805 |
| recall @ 500  | 0.1550 | 0.1690 |
| nDCG @ 100    | 0.1267 | 0.1343 |

We start seeing improvement around `k`=50, when abs(EASE) compensates for missing co-occurrence by utilizing longer chains. 

See `resultsYelp_processed.txt` for full results
