# Personal website and resume builder


Run website locally:

```sh
conda create --name ruby ruby compilers -c conda-forge -y
conda activate ruby
bundle install
jekyll serve --incremental

# or
bundle exec jekyll serve --incremental
```

If things break, try removing `Gemfile.lock`.

Add new posts:

```sh
python new.py POST_NAME
```

Running the script will create a new file in the `_posts` directory.

But you still need to:

1. Move images to `assets/images`
2. Update the paths to the images in the `.md` file


## Resources

* [Jekyll cheatsheet](https://devhints.io/jekyll)
* [Jekyll](https://jekyllrb.com/)
* [Minimal Mistakes template](https://mmistakes.github.io/minimal-mistakes/)
* [Sample website](https://github.com/mmistakes/made-mistakes-jekyll)
* [Serving _pages/ with top paths](https://github.com/jekyll/jekyll/issues/920)
* [Cloudflare settings (SSL and CDN)](https://blog.cloudflare.com/secure-and-fast-github-pages-with-cloudflare/)
* [Email forwarding with Mailgun](https://renzo.lucioni.xyz/mail-forwarding-with-mailgun/)