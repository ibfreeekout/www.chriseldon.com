# www.chriseldon.com
Personal website for Chris Eldon

This repo primarily contains the post content, as well as the necessary components for automating the build process for various include files. As time permits, I will also add other components that are required to this repo for additional clarity. For example, I utilize Server-Side Includes within Nginx for building the various HTML files prior to serving them to the user.

NOTE: This is a highly opinionated and custom-to-me setup. While this is available for use by anyone, it will most likely require some additional modifications to make this work for your own setup.

## Basic requirements

This build script was built with Python 3.15.0. You can install the required modules with the following command:

```
python -m pip install -r requirements.txt
```

## Deploy

To deploy the site, you must first run the script located in `deploy/make.py`. This will create the necessary HTML include files that are used to generate the latest posts list and a few other things on the site. The requirements for this to work is as follows:

- CSV file in `deploy` named `blog_posts.csv`
- HTML files that map to the same date structure as the `blog_posts.csv` file
    - Blog Post entries are structured as `/blog/{year}/{month}/{post_slug}.html`, examples of replacements are below:
        - `{year}` = 2025
        - `{month}` = 03
        - `{post_slug}` = weight-lifting

The `deploy/make.py` file will loop through the `deploy/blog_posts.csv` file to generate links for both the `_site/bloglist.html` and `_site/bloglistfull.html` files, as well as pull out the data from the `<main>` HTML tag within the post itself to generate a valid RSS feed and included it in the `rss.xml` file.

The `templates` folder is used to store template files that `make.py` will retrieve to make modifications and then write to the appropriate `_site` location. The first example of this is with the `templates/footer.html` file. This file contains two dynamic date elements (`%%CUR_DATE%%` and `%%CUR_DATE_LONG%%`) that get replaced when the script runs. `make.py` will retrieve the file, calculate the current date, replace the appropriate strings, and then write the file to the `_site/includes/footer.html` file.

This sort of paradigm can be manipulated with additional functions modeled after the `adjust_footer_date()` function call.

## Uploading content

Once you have confirmed the files have been updated successfully, you can simply copy all of the contents located in the `_site` directory to your website root on the web host.

### Security Notes

This script is by no means intended to be used to accept arbitrary data from anyone other than the owner of a website that would like to use this. Given that it does explicit string replacements, it is theoretically possible for the script to inject just about anything you want based on how it is written. As the owner of your site, it is your responsibility to understand how this code functions and what it is modifying before you run this and upload files to your web host.

#### LLM Development notes

This script was written with the assistance of GitHub Copilot, as well as with experimentation using a locally run qwen3.5:4b model with Ollama.

All post content that makes its way to the public facing website, which includes any and all text - unless otherwise noted and properly sourced in the body of the pages - is the sole creation of me. I do not and will not  use LLMs to generate or assist with writing blog post content or other copy that is intended as human readable output.