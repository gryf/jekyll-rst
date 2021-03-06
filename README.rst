Overview
========

This plugin is a fork of `jekyll-rst <https://github.com/xdissent/jekyll-rst>`_
that adds `ReStructuredText`_ support to `Jekyll`_ and `Octopress`_.  It
renders ReST in posts and pages, and provides a custom directive to support
Octopress-compatible syntax highlighting.

This version supports rst2html5 conversion but hasn't been tested for Octopress
compatability.

The main change on this fork is that this version uses Nokogiri to extract the
HTML body contents since rst2html5 doesn't return parts like rst2html.

There was also cherrypicked changes:

* from `niktwenty3`_

  * cbda0aa Minor edit
  * fe2e42d Updated description about this fork
  * e74e57e Changed converted to use rst2html5 Added rst2html5.py

* from `yingziwu`_

  * 5b8eef7 modify for python3

* from `tranch`_

  z 830d4a4 Remove line number

Requirements
============

* Jekyll *or* Octopress >= 2.0
* Docutils
* Pygments
* `RbST`_
* `nokogiri`_

Installation
============

1. Install Docutils and Pygments.

   The most convenient way is to use virtualenv_burrito:

   ::

      $ curl -s https://raw.github.com/brainsik/virtualenv-burrito/master/virtualenv-burrito.sh | bash
      $ source /Users/xdissent/.venvburrito/startup.sh
      $ mkvirtualenv jekyll-rst
      $ pip install docutils pygments

2. Install RbST.

   If you use `bundler`_ with Octopress, add ``gem 'RbST'`` and ``gem
   'nokogiri'`` to your ``Gemfile`` in the ``development`` group, then run
   ``bundle install``. Otherwise, ``gem install RbST nokogiri``.

3. Install the plugin.

   For Jekyll:

   ::

      $ cd <jekyll-project-path>
      $ git submodule add https://github.com/xdissent/jekyll-rst.git _plugins/jekyll-rst

   For Octopress:

   ::

      $ cd <octopress-project-path>
      $ git submodule add https://github.com/xdissent/jekyll-rst.git plugins/jekyll-rst

4. Start blogging in ReStructuredText. Any file with the ``.rst`` extension
   will be parsed as ReST and rendered into HTML.

   .. note:: Be sure to activate the ``jekyll-rst`` virtualenv before generating
      the site by issuing a ``workon jekyll-rst``. I suggest you follow `Harry
      Marr's advice`_ and create a ``.venv`` file that will  automatically
      activate the ``jekyll-rst`` virtualenv when you ``cd`` into your project.

Source Code Highlighting
========================

A ``code-block`` ReST directive is registered and aliased as ``sourcecode``.
It adds syntax highlighting to code blocks in your documents::

   .. code-block:: ruby

      # Output "I love ReST"
      say = "I love ReST"
      puts say

Optional arguments exist to supply a caption, link, and link title::

   .. code-block:: console
      :caption: Read Hacker News on a budget
      :url: http://news.ycombinator.com
      :title: Hacker News

      $ curl http://news.ycombinator.com | less

Octopress already includes style sheets for syntax highlighting, but you'll
need to generate one yourself if using Jekyll::

   $ pygmentize -S default -f html > css/pygments.css

Octopress Tips
==============

* Use ``.. more`` in your ReST documents to indicate where Octopress's
  ``excerpt`` tag should split your content for summary views.

.. _ReStructuredText: http://docutils.sourceforge.net/rst.html
.. _Jekyll: http://jekyllrb.com/
.. _Octopress: http://octopress.com/
.. _RbST: http://rubygems.org/gems/RbST
.. _bundler: http://gembundler.com/
.. _Harry Marr's advice: http://hmarr.com/2010/jan/19/making-virtualenv-play-nice-with-git/
.. _nokogiri: https://nokogiri.org
.. _niktwenty3: https://github.com/niktwenty3/jekyll-rst2html5
.. _yingziwu: https://github.com/yingziwu/jekyll-rst
.. _tranch: https://github.com/tranch/jekyll-rst
