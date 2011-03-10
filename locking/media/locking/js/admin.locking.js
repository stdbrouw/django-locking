// Set the namespace.
var locking = locking || {};

// Global error function that redirects to the frontpage if something bad
// happens.
locking.error = function() {
	alert(gettext('An unexpected locking error occured. You will be' +
		' forwarded you to a safe place. Sorry!'
	));
	//window.location = '/';
}

// Delays execution of function calls with support for alert(). 
// Takes an array of arrays where the first in each array is the function to 
// call and the second is the delay in seconds. Must be ordered after delays 
// descending, and can only be called once.
locking.delay_execution = function(funcs) {
	var self = this;
	var begin_time = new Date().getTime();
	var funcs = funcs;
	var execute = function() {
		var current_time = new Date().getTime();
		var delay = funcs[0][1];
		if ((current_time-begin_time) / 1000 > delay) {
			funcs[0][0]();
			funcs.shift();
			if (funcs.length === 0) clearInterval(self.interval_id);
		}
	}
	this.interval_id = setInterval(execute, 200);
	execute();
}

// Handles locking on the contrib.admin edit page.
locking.admin = function() {
	// Needs a try/catch here as well as errors does not propagate outside the
	// onready call.
	try {
		settings = locking.settings;
		// Lock only works on change-form pages, not for inline edits in the 
		//list view.
		if (!($("body").hasClass("change-form"))) return;
		
		// Don't apply locking when adding content.
		var id = $.url.segment(3);
		if (id == 'add') return;
		
		var app = $.url.segment(1);
		var model = $.url.segment(2);
		
		// Urls.
		var base_url = settings.base_url + "/" + [app, model, id].join("/");
		var urls = {};
		urls.is_locked = base_url + "/is_locked/";
		urls.lock = base_url + "/lock/";
		urls.unlock = base_url + "/unlock/";
		
		// Texts.
		var text = {};
		
		text.warn = gettext('Your lock on this page expires in less than %s' +
			' minutes. Either save the page or refresh it' + 
			' (hit the F5 button) to renew your lock.')
		;
		text.is_locked = gettext('This page is locked by <em>%(for_user)s' + 
			'</em>. you can view the content but not edit it.');
		text.has_expired = gettext('Your lock on this page is expired.' + 
			' Reload the page to renew it.');

		// Displays a warning that the page is about to expire.
		var display_warning = function() {
			minutes = Math.round((settings.time_until_expiration - 
				settings.time_until_warning) / 60);
			if (minutes < 1) minutes = 1;
			alert(interpolate(text.warn, [minutes]));
		};
		
		// Displays notice on top of page that the page is locked by someone 
		// else.
		var display_islocked = function(data) {
			var notice = '<p class="is_locked">' +
				interpolate(text.is_locked, data, true)
				+ '</p>';
			$("#content-main").prepend(notice);
		}
		
		// Disables all form elements.
		var disable_form = function() {
			$(":input").attr("disabled", "disabled");
		};
		
		// Enables all form elements.
		// TODO: Falsely enables previously disabled form elements.
		var enable_form = function() {
			$(":input").removeAttr("disabled");
		}
		
		// The user did not save in time, expire the page.
		var expire_page = function() {
			disable_form();
			alert(text.has_expired);
		}
		
		// Request a lock on the page, and unlocks page when the user leaves.
		// Adds delayed execution of user notifications.
		var lock_page = function() {
			var request_lock = function() {
				var parse_request_lock = function(jqXHR, textStatus) {
					if (jqXHR.status === 403) {
						display_islocked();
						return;
					} else if (jqXHR.status === 200) {
						enable_form();
						locking.delay_execution([
							[display_warning, settings.time_until_warning], 
							[expire_page, settings.time_until_expiration]
						]);
					} else {
						locking.error();
					}
				}
				$.ajax({
					url: urls.lock,
					complete: parse_request_lock,
				});
			}
			var request_unlock = function() {
				// We have to assure that our unlock request actually gets
				// through before the user leaves the page, so it shouldn't
				// run asynchronously.
				$.ajax({
					url: urls.unlock,
					async: false,
				})
			};
			request_lock();
			$(window).unload(request_unlock);
		}
		
		// The server gave us locking info. Either lock or keep it unlocked
		// while showing notification.
		var parse_succesful_request = function(data, textStatus, jqXHR) {
			eval('data = ' + data);
			if (!data['applies']) {
				lock_page();
			} else {
				display_islocked(data);
			}
		}
		
		// Polls server for the page lock status.
		var request_locking_info = function() {
			$.ajax({
				url: urls.is_locked,
				success: parse_succesful_request,
				error: locking.error,
			});
		};
		
		// Disable form initially.
		disable_form();
		request_locking_info();
		
	} catch(err) {
		locking.error();
	}
}

// Catches if jquery is not included.
try {
	$(locking.admin);	
} catch(err) {
	locking.error();
}