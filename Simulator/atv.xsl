<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">


    <xsl:template match="navigationItem">
        <a>
            <xsl:attribute name="class">navigationItem</xsl:attribute>
            <xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
            <xsl:attribute name="href"><xsl:value-of select="url"/></xsl:attribute>
            <xsl:value-of select="title"/>
        </a>
    </xsl:template>

    <xsl:template match='atv'>
        <html>

        <head>
            <link href="/main.css" rel="stylesheet" type="text/css"/>
            <xsl:if test="head">
                <xsl:apply-templates select="head/*"/>
            </xsl:if>
        </head>

        <xsl:apply-templates select="*"/> 
    </html>
    </xsl:template>

    <xsl:template match="head">
    </xsl:template>

    <xsl:template match="stash">
    </xsl:template>

    <xsl:template match="body">
        <body>
            <div class='mainScreen'>
            <xsl:apply-templates select="@*|node()"/>
            </div>
        </body>
    </xsl:template>


    <xsl:template match='collectionDivider|smallCollectionDivider|horizontalDivider|textDivider'>
        <div class='collectionDivider'>
            <div class='dividerBox'></div>
            <div class='dividerTitleBox'>
                <xsl:attribute name='style'>
                    <xsl:text>text-align:</xsl:text><xsl:value-of select='@alignment'/>
                </xsl:attribute>

            <div class='dividerTitle'>
                <xsl:value-of select='title'/>
            </div>
        </div>
        </div>
    </xsl:template>



    <xsl:template match="header">
        <div class='header'>
        <xsl:apply-templates select="@*|node()"/>
        </div>
    </xsl:template>


    <xsl:template match='simpleHeader'>
        <div class='simpleHeaderMain'>
            <xsl:value-of select="title"/>
            <xsl:if test="image">
                <img class="headerImg">
                    <xsl:attribute name='src'><xsl:value-of select="image"/></xsl:attribute>
                </img>
            </xsl:if>
        </div>
        <xsl:if test='subtitle'>
            <div class='simpleHeaderSub'>
                <xsl:value-of select="subtitle"/>
            </div>
        </xsl:if>
    </xsl:template>

    
    <xsl:template match="menu">
        <div class='menu'>
            <xsl:apply-templates select="@*|node()"/>
        </div>
    </xsl:template>



    <xsl:template match="moviePoster">
        <div class="moviePoster">
            <xsl:attribute name="id">
                <xsl:value-of select="@id"/>
            </xsl:attribute>
            <a>
                <xsl:attribute name='href'><xsl:value-of select='substring-before(substring-after(@onSelect, "&apos;"),"&apos;);")'/></xsl:attribute>
                <img>
                    <xsl:attribute name='src'><xsl:value-of select='image'/></xsl:attribute>
                </img>
                <xsl:if test='title'>
                    <br/><div class='posterTitle'><xsl:value-of select="title"/></div>
                </xsl:if>

            </a>
        </div>
    </xsl:template>



    <xsl:template match="squarePoster">
        <div class="squarePoster">
            <xsl:attribute name="id">
                <xsl:value-of select="@id"/>
            </xsl:attribute>
            <a>
                <xsl:attribute name='href'><xsl:value-of select='substring-before(substring-after(@onSelect, "&apos;"),"&apos;")'/></xsl:attribute>
                <img>
                    <xsl:attribute name='src'><xsl:value-of select='image'/></xsl:attribute>
                </img>
                <xsl:if test='title'>
                    <br/><div class='posterTitle'><xsl:value-of select="title"/></div>
                </xsl:if>

            </a>
        </div>
    </xsl:template>

    <xsl:template match="sixteenByNinePoster">
        <div class="sixteenByNinePoster">
            <xsl:attribute name="id">
                <xsl:value-of select="@id"/>
            </xsl:attribute>
            <a>
                <xsl:attribute name='href'><xsl:value-of select='substring-before(substring-after(@onSelect, "&apos;"),"&apos;);")'/></xsl:attribute>
                <img>
                    <xsl:attribute name='src'>
                        <xsl:choose>
                            <xsl:when test='image/@src1080'><xsl:value-of select='image/@src1080'/></xsl:when>
                            <xsl:when test='image/@src720'><xsl:value-of select='image/@src720'/></xsl:when>
                            <xsl:otherwise><xsl:value-of select='image'/></xsl:otherwise>
                        </xsl:choose>
                    </xsl:attribute>
                </img>
                <xsl:if test='title'>
                    <br/><div class='posterTitle'><xsl:value-of select="title"/></div>
                </xsl:if>

            </a>
        </div>
    </xsl:template>



    <xsl:template match="shelf">
        <div>
            <xsl:attribute name='class'>
                <xsl:choose>
                    <xsl:when test='@columnCount=5'>shelf_five</xsl:when>
                    <xsl:otherwise>shelf</xsl:otherwise>
                </xsl:choose>
            </xsl:attribute>
            <div class='shelfContents'>
                <xsl:apply-templates select="@*|node()"/>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="centerShelf">
        <div class='centerShelf'>
            <div class='shelfContents'>
                <xsl:apply-templates select="@*|node()"/>
            </div>
        </div>
    </xsl:template>


    <xsl:template match="oneLineMenuItem">
        <li class="oneLineMenuItem">
            <xsl:attribute name="id">
                <xsl:value-of select="@id"/>
            </xsl:attribute>
            <a>

                <xsl:attribute name='href'>
                    <xsl:if test='@onSelect'><xsl:value-of select='substring-before(substring-after(@onSelect, "&apos;"),"&apos;);")'/></xsl:if>
                    <xsl:if test='preview/link'><xsl:value-of select='preview/link'/></xsl:if>
                </xsl:attribute>

                <xsl:value-of select='label'/>
            </a>
        </li>

    </xsl:template>


    <xsl:template match="twoLineMenuItem">
        <li class="twoLineMenuItem">
            <xsl:attribute name="id">
                <xsl:value-of select="@id"/>
            </xsl:attribute>
            <a>

                <xsl:attribute name='href'>
                    <xsl:if test='@onSelect'><xsl:value-of select='substring-before(substring-after(@onSelect, "&apos;"),"&apos;);")'/></xsl:if>
                    <xsl:if test='preview/link'><xsl:value-of select='preview/link'/></xsl:if>
                </xsl:attribute>

                <div class='title'><xsl:value-of select='label'/></div>
                <div class='rightlabel'><xsl:value-of select='rightLabel'/></div>                
                <div class='subtitle'><xsl:value-of select='label2'/></div>                

            </a>
        </li>
    </xsl:template>


    <xsl:template match='preview/scrollerPreview'>
            <xsl:apply-templates select="items/grid"/>
    </xsl:template>

    <xsl:template match='preview'>
        <div class='preview'>
            <xsl:apply-templates select="@*|node()"/>
        </div>
    </xsl:template>  


    <xsl:template match='paradePreview'>
        <div class='parade'>
            <ul class='paradePanes'>
                <xsl:for-each select='image'>
                    <li><img><xsl:attribute name='src'><xsl:value-of select='.'/></xsl:attribute></img></li>
                </xsl:for-each>
            </ul>
        </div>
    </xsl:template>

    <xsl:template match="itemDetail">
        <div class='itemDetail'>
            <xsl:apply-templates select="@*"/>
            <div class="detailTop">
            <div class="detailPosterBox">
            <div class="detailPoster">
                <img>
                        <xsl:attribute name='src'><xsl:value-of select="image"/></xsl:attribute>
                        <xsl:attribute name='class'>previewImg <xsl:value-of select="image/@style"/></xsl:attribute>
                </img>
                <div class='detailFootnote'><xsl:value-of select='footnote'/></div>
            </div>
            </div>
            <div>
                <div class='detailHeader'>
                    <div class='headerTitles'>
                        <div class='detailTitle'><xsl:value-of select="title"/></div>
                        <div class='detailSubtitle'><xsl:value-of select="subtitle"/></div>
                    </div>
                    <div class='detailRating'>
                        <img>
                            <xsl:attribute name='src'>/images/apple/Rated_<xsl:value-of select='rating'/>.png</xsl:attribute>
                        </img>
                    </div>
                </div>
                <div class='detailSummary'><hr/><xsl:value-of select="summary"/></div>
                <div class='detailTable'><table>
                    <xsl:apply-templates select="table/columnDefinitions"/>
                    <xsl:apply-templates select="table/rows"/>                    
                </table></div>
                <div class='centerShelf'>
                    <xsl:apply-templates select='centerShelf/shelf'/>
                </div>
            </div>
            </div>
            <xsl:apply-templates select="node()"/> 
        </div>
    </xsl:template>

    <xsl:template match='itemDetail/subtitle'></xsl:template>
    <xsl:template match='itemDetail/footnote'></xsl:template>
    <xsl:template match='itemDetail/rating'></xsl:template>

    <xsl:template match='itemDetail/defaultImage'></xsl:template>
    <xsl:template match='itemDetail/title'></xsl:template>
    <xsl:template match='itemDetail/summary'></xsl:template>
    <xsl:template match='itemDetail/image'></xsl:template>
    <xsl:template match='itemDetail/table'></xsl:template>
    <xsl:template match='itemDetail/centerShelf'></xsl:template>

    <xsl:template match="columnDefinitions">
        <tr>
        <xsl:apply-templates select="@*|node()"/>
        </tr>
    </xsl:template>


    <xsl:template match='columnDefinition'>
        <td class='detailTableColumn' style='color:grey;'>
            <xsl:value-of select="title"/>
        </td>
    </xsl:template>


    <xsl:template match='row'>
        <tr>
            <xsl:for-each select='*'>
                <td><xsl:value-of select='.'/></td>
            </xsl:for-each>
<!--            <xsl:apply-templates select="@*|node()"/>-->
        </tr>
    </xsl:template>  

    <xsl:template match='actionButton'>
       <a>
            <xsl:attribute name='href'>
                <xsl:value-of select='substring-before(substring-after(@onSelect, "&apos;"),"&apos;);")'/>
            </xsl:attribute>
            <div>
                <xsl:attribute name='id'><xsl:value-of select='@id'/></xsl:attribute>
                <xsl:attribute name='class'>actionButton actionButton<xsl:value-of select='substring-before(substring-after(image,"//"), ".")'/></xsl:attribute>    
                <xsl:value-of select='title'/>        
            </div>
       </a>
    </xsl:template>

    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>


    <xsl:template match='videoPlayer'>
        <video>
            <xsl:attribute name='controls'></xsl:attribute>
            <xsl:attribute name='src'>HTTP<xsl:value-of select='substring-after(*/mediaURL, "http")'/></xsl:attribute>
        </video>
    </xsl:template>

</xsl:stylesheet>