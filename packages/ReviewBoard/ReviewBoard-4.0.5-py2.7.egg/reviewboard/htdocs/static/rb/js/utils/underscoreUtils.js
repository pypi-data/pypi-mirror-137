"use strict";

function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

function _iterableToArrayLimit(arr, i) { var _i = arr == null ? null : typeof Symbol !== "undefined" && arr[Symbol.iterator] || arr["@@iterator"]; if (_i == null) return; var _arr = []; var _n = true; var _d = false; var _s, _e; try { for (_i = _i.call(arr); !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

/**
 * Bind callbacks to a context.
 *
 * Backbone.js's various ajax-related functions don't take a context
 * with their callbacks. This allows us to wrap these callbacks to ensure
 * we always have a desired context.
 *
 * Args:
 *     callbacks (object):
 *         An object which potentially includes callback functions.
 *
 *     context (any type):
 *         The context to bind to the callbacks.
 *
 *     methodNames (Array of string):
 *         An array of method names within ``callbacks`` to bind.
 *
 * Returns:
 *     object:
 *     A copy of the ``callbacks`` object, with the given ``methodNames`` bound
 *     to ``context``.
 */
_.bindCallbacks = function (callbacks, context) {
  var methodNames = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : ['success', 'error', 'complete'];

  if (!context) {
    return callbacks;
  }

  var wrappedCallbacks = {};

  for (var _i = 0, _Object$entries = Object.entries(callbacks); _i < _Object$entries.length; _i++) {
    var _Object$entries$_i = _slicedToArray(_Object$entries[_i], 2),
        key = _Object$entries$_i[0],
        value = _Object$entries$_i[1];

    if (methodNames.includes(key) && _.isFunction(value)) {
      wrappedCallbacks[key] = _.bind(value, context);
    }
  }

  return _.defaults(wrappedCallbacks, callbacks);
};
/**
 * Return a function that will be called when the call stack has unwound.
 *
 * This will return a function that calls the provided function using
 * :js:func:`_.defer`.
 *
 * Args:
 *     func (function):
 *         The function to call.
 *
 * Returns:
 *     function:
 *     The wrapper function.
 */


_.deferred = function (func) {
  return function () {
    _.defer(func);
  };
};
/**
 * Return a function suitable for efficiently handling page layout.
 *
 * The returned function will use :js:func:`window.requestAnimationFrame` to
 * schedule the layout call. Once this function called, any subsequent calls
 * will be ignored until the first call has finished the layout work.
 *
 * Optionally, this can also defer layout work until the call stack has unwound.
 *
 * This is intended to be used as a resize event handler.
 *
 * Args:
 *     layoutFunc (function):
 *         The function to call to perform layout.
 *
 *     options (object):
 *         Options for the layout callback.
 *
 * Option Args:
 *     defer (boolean):
 *         If ``true``, the layout function will be called when the call stack
 *         has unwound after the next scheduled layout call.
 */


_.throttleLayout = function (layoutFunc) {
  var options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};
  var handlingLayout = false;
  /*
   * We don't want to use a fat arrow function here, since we need the
   * caller's context to be preserved.
   */

  return function () {
    if (handlingLayout) {
      return;
    }

    var context = this;
    var args = arguments;
    handlingLayout = true;

    var cb = function cb() {
      layoutFunc.apply(context, args);
      handlingLayout = false;
    };

    if (options.defer) {
      cb = _.deferred(cb);
    }

    requestAnimationFrame(cb);
  };
};
/*
 * Return the parent prototype for an object.
 *
 * Args:
 *     obj (object):
 *         An object.
 *
 * Returns:
 *     object:
 *     The object which is the parent prototype for the given ``obj``. This is
 *     roughly equivalent to what you'd get from ES6's ``super``.
 */


window._super = function (obj) {
  return Object.getPrototypeOf(Object.getPrototypeOf(obj));
};

//# sourceMappingURL=underscoreUtils.js.map