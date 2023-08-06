<?xml version="1.0" encoding="UTF-8"?>

<!--
This stylesheet transforms Coverage XML export for iSYSTEM winIDEA
to XML in Cobertura format, so that it can be used by Cobertura
plugin for Jenkins. Since Cobertura is implemented for Java, the
following mapping was introduced to show C coverage info:
- download file (executable, usually elf file) is mapped to packages
- source file is mapped to class, because in Java one file usually
  contains one class.
- C functions are mapped to methods
- C lines are equvalent to Java source lines
- each condition can be executed as true, false, or both.
  iSYSTEM coverage provides this information, and to show it in Cobertura
  format, number of conditions is multipled by 2. Condition coverage is then
  calculated as:
  (true + false + both *2) / (cn * 2)

  To provide enough information in coverage file, the following information
  must be preent in XML export file:

  - Measure all functions must be checked
  - Function lines must be exported (YES)

  Sources are not needed and are not shown in Jenkins. For this level of detail
  in coverage, export coverage in iSYSTEM HTML format.

  Meaning of coverture attributes:
  line-rate: line coverage in range [0..1], where 1 means 100% coverage
-->

<xsl:stylesheet id='isystemTestReportXslt' version="2.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xpath-default-namespace="https://resources.isystem.com/analyzer_coverage_export">
    
  <xsl:output method="xml" encoding="utf-8"
              doctype-system="http://cobertura.sourceforge.net/xml/coverage-04.dtd"/>

  <xsl:template match="/">
    <coverage timestamp="{/coverage/info/date} -  {/coverage/info/time}"
              line-rate="{/coverage/images/lx div /coverage/images/l}"
              branch-rate="{(/coverage/images/cn1 + /coverage/images/cn0 + /coverage/images/cn01 * 2) div (/coverage/images/cn * 2)}"
              lines-covered="{/coverage/images/lx}"
              lines-valid="{/coverage/images/l}"
              branches-covered="{(/coverage/images/cn1 + /coverage/images/cn0 + /coverage/images/cn01 * 2) div 2}"
              branches-valid="{/coverage/images/cn}"
              complexity="{/coverage/images/cn + 1}"
              version="{/coverage/info/software}"
    >
    <xsl:text>&#xa;</xsl:text>
    
      <packages>
          <xsl:apply-templates select="coverage/images/image"/>
      </packages>

    </coverage>
  </xsl:template>


  <xsl:template match="coverage/images/image">
    <xsl:text>&#xa;</xsl:text>
    <package name="{name}"
             line-rate="{lx div l}"
             branch-rate="{(cn1 + cn0 + cn01 * 2) div (cn*2)}"
             complexity="{cn + 1}"
             >
      <xsl:text>&#xa;</xsl:text>
      <classes>
        <xsl:apply-templates select="folder"/>
      </classes>
      <xsl:text>&#xa;</xsl:text>
    </package>
  </xsl:template>


  <xsl:template match="coverage/images/image/folder">
    <xsl:apply-templates select="module"/>
  </xsl:template>


  <xsl:template match="coverage/images/image/folder/module">
    <xsl:text>&#xa;</xsl:text>  
    <class name="{name}" filename="{rel_path}"
             line-rate="{lx div l}"
             branch-rate="{(cn1 + cn0 + cn01 * 2) div (cn*2)}"
             complexity="{cn + 1}"
             >
      <xsl:text>&#xa;</xsl:text>
      <methods>
        <xsl:apply-templates select="fn"/>
      </methods>
      <xsl:text>&#xa;</xsl:text>
      <lines>
        <xsl:apply-templates select="fn/ln"/>
      </lines>
      <xsl:text>&#xa;</xsl:text>
    </class>
  </xsl:template>


  <xsl:template match="coverage/images/image/folder/module/fn">
      <xsl:text>&#xa;</xsl:text>
      <xsl:text>&#xa;</xsl:text>
      <method name="{name}" signature=""
             line-rate="{lx div l}"
             branch-rate="{(cn1 + cn0 + cn01 * 2) div (cn*2)}"
             complexity="{cn + 1}"
      >
      <xsl:text>&#xa;</xsl:text>
      <lines>
        <xsl:apply-templates select="ln"/>
      </lines>
      <xsl:text>&#xa;</xsl:text>
    </method>
  </xsl:template>


  <xsl:template match="ln">
      <xsl:text>&#xa;</xsl:text>
      <xsl:choose>
          <xsl:when test="cn = 0">
              <line number="{sn}" hits="{ec}" branch="false"
                    condition-coverage="0%"/>
          </xsl:when>
          <xsl:otherwise>
              <line number="{sn}" hits="{ec}" branch="true"
                    condition-coverage="{(cn1 + cn0 + cn01 * 2) div (cn*2) *100}%"/>
          </xsl:otherwise>
      </xsl:choose>
  </xsl:template>

  <!-- condition node is ignored, because Jenkins plugin takes information from
       the string above.
       -->
</xsl:stylesheet>
