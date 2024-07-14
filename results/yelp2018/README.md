## Results highlights
|               | EASE          | abs(EASE)     |  lift  |  p-value  |
| ------------- | ------------- | ------------- | ------ | ------ |
| recall @ 20   | 0.0553 | 0.0552 | -0.000152 | 0.433676 |
| nDCG @ 20     | 0.0801 | 0.0798 | -0.000332 | 0.148517 |
| recall @ 50   | 0.1044 | 0.1055 | +0.001050 | 0.000039 |
| nDCG @ 50     | 0.1161 | 0.1166 | +0.000527 | 0.026162 |
| recall @ 100  | 0.1616 | 0.1653 | +0.003726 | 0.000000 |
| nDCG @ 100    | 0.1508 | 0.1528 | +0.002041 | 0.000000 |
| recall @ 500  | 0.3663 | 0.3964 | +0.030174 | 0.000000 |
| nDCG @ 500    | 0.2500 | 0.2637 | +0.013717 | 0.000000 |

We start seeing improvement around `k`=50, when abs(EASE) compensates for missing co-occurrence by utilizing longer chains. 

See `resultsYelp_processed.txt` for full results
