require 'rbst'
require 'nokogiri'

module Jekyll
  class RestConverter < Converter
    safe true

    priority :low

    def matches(ext)
      ext =~ /^\.rst$/i
    end

    def output_ext(ext)
      ".html"
    end

    def convert(content)
      dirname = "#{File.expand_path(File.dirname(__FILE__))}"
      RbST.executables = {:html => dirname + "/rst2html5.py"}
      level = 2

      conf = Jekyll.configuration({})
      if conf.has_key?('rst')
        level = conf['rst']['initial_header_level']
        if not level.is_a?(Integer)
          level = 2
        end
      end

      rst2htmlcontent = RbST.new(content).to_html(:initial_header_level => level)
      document = Nokogiri::HTML(rst2htmlcontent)
      content = document.css('body').inner_html
    end
  end

  module Filters
    def restify(input)
      site = @context.registers[:site]
      converter = site.getConverterImpl(Jekyll::RestConverter)
      converter.convert(input)
    end
  end
end
