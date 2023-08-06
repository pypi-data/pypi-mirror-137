var captcha_passed = false;

function set_listeners() {
	var ids = ["a", "b", "c", "d", "e", "f"];
	var regions = ["u", "e", "j", "k"];
	for (var i = 0; i < ids.length; i++) {
        document.getElementById(ids[i]).addEventListener("keydown", keyHandler);
        document.getElementById(ids[i]).addEventListener("keydown", moveInputFocus);
        document.getElementById(ids[i]).addEventListener("keyup", update);
	}
	for (var i = 0; i < regions.length; i++) {
		var x = (i + 1 === regions.length) ? i : i;
		document.getElementById("region_" + regions[x]).addEventListener("click", update);
	}
}

function keyHandler(e) {
	var keycode = window.event ? event.keyCode : event.which;
	console.log("Alphanum:", check_key_alphanum(e));
	console.log("Navigation:", check_key_nav(e));
	console.log("Modifier:", check_key_mod(e));
	console.log("Arrow can move:", check_arrow_movable(e));
	return !check_arrow_movable(e) &&
		(check_key_alphanum(e) ||
			check_key_nav(e) ||
			check_key_mod(e)
		) ? true : e.preventDefault();
}

function check() {
	var ids = ["a", "b", "c", "d", "e", "f"];
	var total = "";
	for (var i = 0; i < 6; i++) {
		total += document.getElementById(ids[i]).value;
	}
	if (total.match(/^[0-9a-f]{12}$/igm) == null) {
		return false;
	}
	var regions = ["u", "e", "j", "k"];
	var count = 0;
	for (var i = 0; i < regions.length; i++) {
		if (document.getElementById("region_" + regions[i]).checked === false) {
			count++;
		}
		if (count === 4) {
			return false;
		}
	}
	if (document.getElementById("recaptcha") === null) {
		return true;
	} else {
		return captcha_passed;
	}
}

function update() {
	var ok = check();
	document.getElementById("submit_btn").disabled = !ok;
	document.getElementById("submit_btn2").disabled = !ok;
	document.getElementById("submit_btn3").disabled = !ok;
	document.getElementById("submit_btn4").disabled = !ok;
}

function moveInputFocus(e) {
	var ids = ["a", "b", "c", "d", "e", "f"];
	var index = (ids.indexOf(event.target.id.toLowerCase()) + 1 === ids.length) ?
		null : ids[ids.indexOf(event.target.id) + 1];
	if (e.target.textLength === 2 && check_key_onlyalpha(e) && index !== null) {
		document.getElementById(index).value = "";
		document.getElementById(index).focus();
		document.getElementById(index).setSelectionRange(0, 0, "forward");
		return true;
	} else if (check_arrow_movable(e)) {
		var keycode = window.event ? event.keyCode : event.which;
		if (keycode === 37) {
			var x = ids.indexOf(event.target.id.toLowerCase()) === 0 ?
				null : ids[ids.indexOf(event.target.id) - 1];
			if (x !== null) {
				document.getElementById(x).focus();
				document.getElementById(x).setSelectionRange(2, 2, "backward");
				return true;
			} else {
				return false;
			}
		} else if (keycode === 39) {
			var x = (ids.indexOf(event.target.id.toLowerCase()) + 1 === ids.length) ?
				null : ids[ids.indexOf(event.target.id) + 1];
			if (x !== null) {
				document.getElementById(x).focus();
				document.getElementById(x).setSelectionRange(0, 0, "forward");
				return true;
			} else {
				return false;
			}
		}
	} else {
		return false;
	}
}

function check_key_alphanum(e) {
	var keycode = window.event ? event.keyCode : event.which;
	return (48 <= keycode && keycode <= 57) || (65 <= keycode && keycode <= 70);
}

function check_key_nav(e) {
	var keycode = window.event ? event.keyCode : event.which;
	return 37 <= keycode && keycode <= 40 || keycode === 8 || keycode === 9 || keycode === 46 || keycode === 35 ||
		keycode === 36;
}

function check_key_mod(e) {
	var keycode = window.event ? event.keyCode : event.which;
	return keycode === 16 || keycode === 20 || keycode === 17 || keycode === 18;
}

function check_key_onlyalpha(e) {
	return check_key_alphanum(e) && !check_key_nav(e) && !check_key_mod(e);
}

function check_arrow_movable(e) {
	var keycode = window.event ? event.keyCode : event.which;
	console.debug("Checking if arrow is movable:", e);
	if (keycode === 37) {
		if (e.target.textLength === 2) {
			return e.target.selectionStart === 0;
		} else if (e.target.textLength === 1) {
			return e.target.selectionStart === 0;
		} else {
			return e.target.textLength === 0;
		}
	} else if (keycode === 39) {
		if (e.target.textLength === 2) {
			return e.target.selectionStart === 2;
		} else if (e.target.textLength === 1) {
			if (e.target.selectionStart === 1) {
				return true;
			}
		} else if (e.target.textLength === 0) {
			return true;
		}
	} else {
		return false;
	}
}

function captcha_ok() {
	captcha_passed = true;
	update();
}

function captcha_expired() {
	captcha_passed = false;
	update();
}

window.onload = update;
set_listeners();