Add-Type -AssemblyName System.Drawing
$base=Join-Path $PSScriptRoot 'assets'
$bmp=[Drawing.Bitmap]::new(1200,1200)
$g=[Drawing.Graphics]::FromImage($bmp)
$g.Clear([Drawing.ColorTranslator]::FromHtml('#FAF9F5'))
$g.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$g.TextRenderingHint=[Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$green=[Drawing.ColorTranslator]::FromHtml('#196633')
$ink=[Drawing.ColorTranslator]::FromHtml('#20382B')
$muted=[Drawing.ColorTranslator]::FromHtml('#647168')
function T($s,$x,$y,$size,$c,$bold=$false){
 $style=if($bold){[Drawing.FontStyle]::Bold}else{[Drawing.FontStyle]::Regular}
 $f=[Drawing.Font]::new('Segoe UI',$size,$style,[Drawing.GraphicsUnit]::Pixel)
 $b=[Drawing.SolidBrush]::new($c);$g.DrawString($s,$f,$b,[single]$x,[single]$y);$b.Dispose();$f.Dispose()
}
$photo=[Drawing.Image]::FromFile((Join-Path $PSScriptRoot '../social-media-mockups/assets/saif-facility-clean.jpg'))
$g.DrawImage($photo,[Drawing.Rectangle]::new(0,0,1200,620),[Drawing.Rectangle]::new(0,280,4000,2067),[Drawing.GraphicsUnit]::Pixel)
$photo.Dispose()
T 'SAIF INDUSTRIES LLC' 60 663 25 $green $true
T 'Aerospace supply.' 54 712 68 $ink $true
T 'Built on experience.' 54 794 68 $ink $true
$pen=[Drawing.Pen]::new([Drawing.ColorTranslator]::FromHtml('#CAD5CA'),1)
$g.DrawLine($pen,60,914,1140,914)
T '1999' 60 941 45 $green $true
T 'Family-owned since' 60 1004 21 $muted
T '200,000+' 410 941 45 $green $true
T 'Unique parts in inventory' 410 1004 21 $muted
T '44,000 sq. ft.' 813 941 45 $green $true
T 'Facility' 816 1004 21 $muted
T 'Explore the business behind aerospace parts sourcing.' 60 1071 27 $ink
T 'saifindustries.com' 60 1140 23 $green
T 'WEBSITE PHOTO / STUDENT AD CONCEPT' 731 1147 16 $muted
$bmp.Save((Join-Path $base 'investor-ad.png'),[Drawing.Imaging.ImageFormat]::Png)
$pen.Dispose();$g.Dispose();$bmp.Dispose()
Write-Output 'Created investor and strategic-partner awareness ad using the real SAIF website photo.'
