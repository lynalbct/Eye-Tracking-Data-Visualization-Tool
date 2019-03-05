$('#pop-code').on('click', function generateCode(){
    popOpen($('#pop-code')); // Code view popup output
    
    var imgsrc = ($('#workspace-img').attr('src').slice(0, 4) == 'blob') ? '<em>filepath</em>' : $('#workspace-img').attr('src'); // 이미지 소스
    var gcAloop = ''; // A Tag Markup Loop
    var gcMloop = ''; // 이Image map markup loop
    var gcAlert = '<em class="pop-content-alert">&#9888; You have to replace each red text with a value.</em>';

    for (i=0;i<cnt;i++) {
        // A Tag shape coordinates and size
        var top = (unit == 'px') ? $('#grid-box-' + i).position().top + 1 : ($('#grid-box-' + i).position().top / (imgHeight - 2) * 100).toFixed(2);
        var left = (unit == 'px') ? $('#grid-box-' + i).position().left + 1 : ($('#grid-box-' + i).position().left / (imgWidth - 2) * 100).toFixed(2);
        var width = (unit == 'px') ? $('#grid-box-' + i).width() : ($('#grid-box-' + i).width() / imgWidth * 100).toFixed(2);
        var height = (unit == 'px') ? $('#grid-box-' + i).height() : ($('#grid-box-' + i).height() / imgHeight * 100).toFixed(2);
        
        // Image map shape coordinates (px only)
        var startCoordX = parseInt($('#grid-box-' + i).position().left + 1);
        var startCoordY = parseInt($('#grid-box-' + i).position().top + 1);
        var endCoordX = parseInt(startCoordX + $('#grid-box-' + i).width() + 1); // +1 is the actual correction value
        var endCoordY = parseInt(startCoordY + $('#grid-box-' + i).height() + 1);
        
        var link = (mapEl[i][2]) ? mapEl[i][2] : '<em>link</em>';
        var target = (mapEl[i][3]) ? mapEl[i][3] : '<em>target</em>';
        localStorage.setItem('startCoordX');
        localStorage.setItem('startCoordY');
        localStorage.setItem('endCoordX');
        localStorage.setItem('endCoordY');

        
        // 마크업 루프 생성
        gcAloop += '&nbsp;&nbsp;&nbsp;&nbsp;&lt;a href="' + link + '" style="position:absolute; top:' + top + unit + '; left:' + left + unit + '; width:' + width + unit + '; height:' + height + unit + '; display:block; background:url(about:blank);"&gt;&lt;a&gt;' + '<br>';
        gcMloop += '&nbsp;&nbsp;&nbsp;&nbsp;&lt;area shape="rect" coords="' + startCoordX + ', ' + startCoordY + ', ' + endCoordX + ', ' + endCoordY + '" href="' + link + '" target="' + target + '"&gt;' + '<br>';
    }
    
    // A 태그 마크업
    var gcA = gcAlert + '&lt;div style="position:relative"&gt;' + '<br>' + '&nbsp;&nbsp;&nbsp;&nbsp;&lt;img src="' + imgsrc + '"&gt;' + '<br>' + gcAloop + '&lt;/div&gt;';
    $('#pop-codegen-a .pop-content p').html(gcA); // 생성된 마크업 출력
    
    // 이미지맵 마크업
    var gcM = gcAlert + '&lt;img src="' + imgsrc + '" usemap="#<em>mapname</em>"&gt;' + '<br>' + '&lt;map name="<em>mapname</em>"&gt;' + '<br>' + gcMloop + '&lt;/map&gt;';
    $('#pop-codegen-im .pop-content p').html(gcM); // 생성된 마크업 출력

    $.ajax({
        type: 'POST',
        url: '/crop'

    });
});


popOpen($('#pop-code')); // Code view popup output
    
    var imgsrc = ($('#workspace-img').attr('src').slice(0, 4) == 'blob') ? '<em>filepath</em>' : $('#workspace-img').attr('src'); // 이미지 소스
    var gcAloop = ''; // A Tag Markup Loop
    var gcMloop = ''; // 이Image map markup loop
    var gcAlert = '<em class="pop-content-alert">&#9888; You have to replace each red text with a value.</em>';

    for (i=0;i<cnt;i++) {
        // A Tag shape coordinates and size
        var top = (unit == 'px') ? $('#grid-box-' + i).position().top + 1 : ($('#grid-box-' + i).position().top / (imgHeight - 2) * 100).toFixed(2);
        var left = (unit == 'px') ? $('#grid-box-' + i).position().left + 1 : ($('#grid-box-' + i).position().left / (imgWidth - 2) * 100).toFixed(2);
        var width = (unit == 'px') ? $('#grid-box-' + i).width() : ($('#grid-box-' + i).width() / imgWidth * 100).toFixed(2);
        var height = (unit == 'px') ? $('#grid-box-' + i).height() : ($('#grid-box-' + i).height() / imgHeight * 100).toFixed(2);
        
        // Image map shape coordinates (px only)
        var startCoordX = parseInt($('#grid-box-' + i).position().left + 1);
        var startCoordY = parseInt($('#grid-box-' + i).position().top + 1);
        var endCoordX = parseInt(startCoordX + $('#grid-box-' + i).width() + 1); // +1 is the actual correction value
        var endCoordY = parseInt(startCoordY + $('#grid-box-' + i).height() + 1);
        
        var link = (mapEl[i][2]) ? mapEl[i][2] : '<em>link</em>';
        var target = (mapEl[i][3]) ? mapEl[i][3] : '<em>target</em>';
        localStorage.setItem('startCoordX');
        localStorage.setItem('startCoordY');
        localStorage.setItem('endCoordX');
        localStorage.setItem('endCoordY');

        
        // 마크업 루프 생성
        gcAloop += '&nbsp;&nbsp;&nbsp;&nbsp;&lt;a href="' + link + '" style="position:absolute; top:' + top + unit + '; left:' + left + unit + '; width:' + width + unit + '; height:' + height + unit + '; display:block; background:url(about:blank);"&gt;&lt;a&gt;' + '<br>';
        gcMloop += '&nbsp;&nbsp;&nbsp;&nbsp;&lt;area shape="rect" coords="' + startCoordX + ', ' + startCoordY + ', ' + endCoordX + ', ' + endCoordY + '" href="' + link + '" target="' + target + '"&gt;' + '<br>';
    }
    
    // A 태그 마크업
    var gcA = gcAlert + '&lt;div style="position:relative"&gt;' + '<br>' + '&nbsp;&nbsp;&nbsp;&nbsp;&lt;img src="' + imgsrc + '"&gt;' + '<br>' + gcAloop + '&lt;/div&gt;';
    $('#pop-codegen-a .pop-content p').html(gcA); // 생성된 마크업 출력
    
    // 이미지맵 마크업
    var gcM = gcAlert + '&lt;img src="' + imgsrc + '" usemap="#<em>mapname</em>"&gt;' + '<br>' + '&lt;map name="<em>mapname</em>"&gt;' + '<br>' + gcMloop + '&lt;/map&gt;';
    $('#pop-codegen-im .pop-content p').html(gcM); // 생성된 마크업 출력
}