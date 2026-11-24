Add-Type -AssemblyName System.Drawing
$base = Join-Path $PSScriptRoot 'assets'
$green = [Drawing.ColorTranslator]::FromHtml('#196633')
$ink = [Drawing.ColorTranslator]::FromHtml('#15271D')
$cream = [Drawing.ColorTranslator]::FromHtml('#F2F5F0')
function Brush($c) { return [Drawing.SolidBrush]::new($c) }
function Text($g,$s,$x,$y,$size,$c,$bold=$false) {
  $style = if ($bold) {[Drawing.FontStyle]::Bold} else {[Drawing.FontStyle]::Regular}
  $f=[Drawing.Font]::new('Arial',$size,$style,[Drawing.GraphicsUnit]::Pixel)
  $b=Brush $c
  $g.DrawString($s,$f,$b,[single]$x,[single]$y)
  $f.Dispose(); $b.Dispose()
}
function Logo($g,$x,$y,$w,$h) {
  [xml]$doc=Get-Content -Raw (Join-Path $base 'saif-logo-green.svg')
  foreach($p in $doc.GetElementsByTagName('path')) {
    $path=[Drawing.Drawing2D.GraphicsPath]::new()
    $tokens=[regex]::Matches($p.d,'[MLZ]|-?\d+(?:\.\d+)?')
    $pts=[Collections.Generic.List[Drawing.PointF]]::new()
    $i=0
    while($i -lt $tokens.Count) {
      $v=$tokens[$i].Value
      if($v -eq 'M') {
        if($pts.Count -gt 2){$path.AddPolygon($pts.ToArray()); $pts.Clear()}
        $i++; continue
      }
      if($v -eq 'L') {$i++; continue}
      if($v -eq 'Z') {
        if($pts.Count -gt 2){$path.AddPolygon($pts.ToArray()); $pts.Clear()}
        $i++; continue
      }
      $px=[single]::Parse($v,[Globalization.CultureInfo]::InvariantCulture)
      $py=[single]::Parse($tokens[$i+1].Value,[Globalization.CultureInfo]::InvariantCulture)
      if($p.ParentNode.GetAttribute('transform') -eq 'rotate(180 500 500)') {
        $px=1000-$px; $py=1000-$py
      }
      $px=$px + [Math]::Tan(-16*[Math]::PI/180)*($py-500)
      $pts.Add([Drawing.PointF]::new(($x+($px+270)/1540*$w),($y+($py-60)/880*$h)))
      $i+=2
    }
    if($pts.Count -gt 2){$path.AddPolygon($pts.ToArray())}
    $b=Brush ([Drawing.ColorTranslator]::FromHtml('#066A3B'))
    $g.FillPath($b,$path); $b.Dispose(); $path.Dispose()
  }
}
function Canvas($w,$h) {
  $bmp=[Drawing.Bitmap]::new($w,$h)
  $g=[Drawing.Graphics]::FromImage($bmp)
  $g.SmoothingMode=[Drawing.Drawing2D.SmoothingMode]::AntiAlias
  $g.TextRenderingHint=[Drawing.Text.TextRenderingHint]::AntiAliasGridFit
  $g.Clear([Drawing.Color]::White)
  return @($bmp,$g)
}
$c=Canvas 1080 1080; $bmp=$c[0]; $g=$c[1]
Logo $g 108 293 864 494
$bmp.Save((Join-Path $base 'profile-picture.png'),[Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()
$cards=@(
  @{file='01-introduction';label='MEET SAIF INDUSTRIES';lines=@('Stocked.','Sourced.','Delivered.');sub='Your aerospace parts connection.';foot='FAMILY-OWNED SINCE 1999';dark=$true},
  @{file='02-parts-sourcing';label='PARTS SOURCING';lines=@('Hard to find?','Start here.');sub='Aerospace sourcing starts with a conversation.';foot='TELL US WHAT YOU NEED';dark=$false},
  @{file='03-quality';label='QUALITY & DOCUMENTATION';lines=@('The details','matter.');sub='Inspection. Documentation. Traceability.';foot='A CLOSER LOOK AT QUALITY';dark=$true},
  @{file='04-facility';label='BEHIND THE INVENTORY';lines=@('Space for','what comes','next.');sub='Inside the SAIF supply operation.';foot='BAKERSFIELD, CALIFORNIA';dark=$false},
  @{file='05-global-support';label='GLOBAL SUPPORT';lines=@('Across borders.','Within reach.');sub='A conversation that connects your supply chain.';foot='LET\u2019S TALK SOURCING';dark=$true},
  @{file='06-request-a-quote';label='START A QUOTE';lines=@('Your next part','starts with','a part number.');sub='Part number + quantity + requirements';foot='SALES@SAIFIND.COM';dark=$false}
)
foreach($card in $cards) {
 $c=Canvas 1080 1080; $bmp=$c[0]; $g=$c[1]
 $bg=if($card.dark){$green}else{$cream}; $fg=if($card.dark){[Drawing.Color]::White}else{$ink}
 $g.Clear($bg)
 $accent=if($card.dark){[Drawing.Color]::FromArgb(55,255,255,255)}else{[Drawing.Color]::FromArgb(35,25,102,51)}
 $pen=[Drawing.Pen]::new($accent,2)
 $g.DrawEllipse($pen,660,200,630,630); $g.DrawEllipse($pen,735,275,480,480)
 $g.DrawLine($pen,620,515,1079,515); $g.DrawLine($pen,975,125,975,900)
 $pen.Dispose()
 Text $g 'SAIF / INDUSTRIES' 72 65 27 $fg $true
 Text $g 'AEROSPACE PARTS & SUPPLY' 72 108 17 $fg
 $b=Brush $fg; $g.FillRectangle($b,72,213,75,6); $b.Dispose()
 Text $g $card.label 72 251 24 $fg $true
 $y=335
 foreach($line in $card.lines){Text $g $line 65 $y 87 $fg $true; $y+=100}
 Text $g $card.sub 72 720 28 $fg
 Text $g ($card.foot -replace '\\u2019',"'") 72 882 23 $fg $true
 Text $g 'saifindustries.com' 72 961 22 $fg
 Text $g 'CLASS PROJECT / CONCEPT' 728 971 15 $fg
 $bmp.Save((Join-Path $base ($card.file+'.png')),[Drawing.Imaging.ImageFormat]::Png)
 $g.Dispose(); $bmp.Dispose()
}
$c=Canvas 2256 382; $bmp=$c[0]; $g=$c[1]; $g.Clear($green)
Text $g 'STOCKED. SOURCED. DELIVERED.' 590 92 66 ([Drawing.Color]::White) $true
Text $g 'Aerospace parts & supply  /  Family-owned since 1999' 596 193 34 ([Drawing.Color]::White)
Text $g 'SAIF INDUSTRIES LLC' 596 276 24 ([Drawing.Color]::White)
Text $g 'CLASS PROJECT / CONCEPT' 1820 334 20 ([Drawing.Color]::White)
$bmp.Save((Join-Path $base 'linkedin-cover.png'),[Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()
Write-Output 'Created profile picture, LinkedIn cover, and six post graphics.'
