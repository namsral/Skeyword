## Skeyword

Unify search engine shortcuts among your web browsers.

If you often switch between web browsers it can be a hassle to keep those search engine shortcuts in sync. Run this web service in the background and you'll be able to access the same search engine shortcuts from all your browsers. It's basically a webproxy written in Python which replaces the default search engine in your browser.


**Requirements**

Just Python, preferebly v2.6.


**Setup**

1. Add your favorite search engines to the keywords.json file
2. Launch a Terminal and run the Skeyword script:

        python skeyword.py --port 8001

3. Open your web browser and browse to http://localhost:8001/

For more options see the help message:

        python skeyword.py --help

