(function () {
	var scener = {
		init : function () {
			$("#main_column .panel").on("click", this.sectionClickHandler);
		},
		sectionClickHandler : function () { 
			var parent = $(this).parent();
			parent.find("table").toggle();
			parent.find(".actions").toggle();
		}
	};

	$(scener.init());

}());
