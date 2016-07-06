The file greek\_english\_lexicon_lsj.xml comes from Perseus, where is was called 1999.04.0057.xml (<http://sourceforge.net/projects/perseus-hopper/>) and licensed under the [Mozilla Public License 1.1 (MPL 1.1)](http://www.mozilla.org/MPL/1.1/).

#### greek-analyses.json
The files `greek-analyses_1/2.json` contains definitions for words present in greek text corpus. The definitions are scraped from the [Perseues](http://www.perseus.tufts.edu/hopper/morph) website using `scraper.py`. The words entries present here are in [Beta code](https://en.wikipedia.org/wiki/Beta_Code) form.
#### Scraping

```
python3 scraper.py <input_filename> <output_filename> <language>
```
The scraper tries to fetch definitions for words present in the input file at start of each line.