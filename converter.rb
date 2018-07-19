require 'rbst'
require 'nokogiri'

module Jekyll
  class RestConverter < Converter
    safe true

    priority :low

    def matches(ext)
      ext =~ /rst/i
    end

    def output_ext(ext)
      ".html"
    end

    def convert(content)
      # RbST.executables = {:html => "/usr/local/bin/rst2html5"}
      RbST.executables = {:html => "#{File.expand_path(File.dirname(__FILE__))}/rst2html5.py"}
      rst2htmlcontent = RbST.new(content).to_html(:initial_header_level => 1)
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
