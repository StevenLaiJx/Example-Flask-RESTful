var selectYear = new Date().getFullYear();
var selectMonth = '';
var yearOrMonthPublic = '';
var dateDiv = '';
function createMonthOrYear(evt){

	var strBody = $("<div><div class='myDatePicker'><div class='selectYear'><div class='left'>&lt;</div><table><tr><td>-11</td><td>-10</td><td>-9</td></tr><tr><td>-8</td><td>-7</td><td>-6</td></tr><tr><td>-5</td><td>-4</td><td>-3</td></tr><tr><td>-2</td><td>-1</td><td class='selectOn'>0</td></tr></table> <div class='right nonePointer'>&gt;</div></div><div class='selectMonth'><table><tr><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td></tr><tr><td>7</td><td>8</td><td>9</td><td>10</td><td>11</td><td>12</td></tr></table></div></div></div>").html();
	$('#mysMonth').html(strBody);
	$('#mysYear').html(strBody);
	var thisYear = new Date().getFullYear();
	$('.myDatePicker .selectYear td').each(function(){
		$(this).html(parseInt($(this).html()) + thisYear);
	});

	$('.myDatePicker .left').not('.nonePointer').click(function(){
		$('.myDatePicker .selectYear td').removeClass('selectOn');
		$('.myDatePicker .right').removeClass('nonePointer');
		$('.myDatePicker .selectYear td').each(function(){
			$(this).html(parseInt($(this).html()) - 12);
			if ($(this).html() == getSelectYear()){$(this).addClass('selectOn');};
		});
	});
	$('.myDatePicker .right').click(function(){
		if (parseInt($('.myDatePicker .selectYear td:last').html()) == thisYear){
			return;
		}
		$('.myDatePicker .selectYear td').removeClass('selectOn');
		$('.myDatePicker .selectYear td').each(function(){
			$(this).html(parseInt($(this).html()) + 12);
			if ($(this).html() == getSelectYear()){$(this).addClass('selectOn');};
			});
			if (parseInt($('.myDatePicker .selectYear td:last').html()) == thisYear){
				$('.myDatePicker .right').addClass('nonePointer');
		}
	});
	
	$('.myDatePicker .selectYear td').click(function(){
		$(this).parents('.myDatePicker').find('td').removeClass('selectOn');
		$(this).addClass('selectOn');
		selectYear = $(this).html();
		if (yearOrMonthPublic == 'year'){
			$('.myDatePicker').hide();
			selectMonth = '';
			evt(selectYear,selectMonth);
		};
	});
	
	$('.myDatePicker .selectMonth td').click(function(){
		$('.myDatePicker .selectMonth td').removeClass('selectOn');
		$(this).addClass('selectOn');
		selectMonth = $(this).html();
		$('.myDatePicker').hide();
		evt(selectYear,selectMonth);
	}); 
}
function selectYearOrMonth(yearOrMonth,dateDiv){
	selectYear = $('#'+dateDiv+' .myDatePicker .selectYear td.selectOn').html();
	selectMonth = $('#'+dateDiv+' .myDatePicker .selectMonth td.selectOn').html();
	yearOrMonthPublic = yearOrMonth;
	$('.myDatePicker').not('#'+dateDiv+' .myDatePicker').hide();
	$('#'+dateDiv+' .myDatePicker').toggle();
	$('.selectMonth').show();
	if (yearOrMonthPublic == 'year'){
		$('.selectMonth').hide();
	};
}
function getSelectYear(){
	return selectYear;
	}
function getSelectMonth(){
	return selectMonth;
}