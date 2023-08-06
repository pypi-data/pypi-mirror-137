"use strict";

function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _iterableToArrayLimit(arr, i) { var _i = arr == null ? null : typeof Symbol !== "undefined" && arr[Symbol.iterator] || arr["@@iterator"]; if (_i == null) return; var _arr = []; var _n = true; var _d = false; var _s, _e; try { for (_i = _i.call(arr); !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

function _createForOfIteratorHelper(o, allowArrayLike) { var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"]; if (!it) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e2) { throw _e2; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = it.call(o); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e3) { didErr = true; err = _e3; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

/**
 * The base model for all API-backed resource models.
 *
 * This provides a common set of attributes and functionality for working
 * with Review Board's REST API. That includes fetching data for a known
 * resource, creating resources, saving, deleting, and navigating children
 * resources by way of a payload's list of links.
 *
 * Other resource models are expected to extend this. In particular, they
 * should generally be extending toJSON() and parse().
 */
RB.BaseResource = Backbone.Model.extend({
  /**
   * Return default values for the model attributes.
   *
   * Returns:
   *     object:
   *     The attribute defaults.
   */
  defaults: function defaults() {
    return {
      extraData: {},
      links: null,
      loaded: false,
      parentObject: null
    };
  },

  /** The key for the namespace for the object's payload in a response. */
  rspNamespace: '',

  /** The attribute used for the ID in the URL. */
  urlIDAttr: 'id',
  listKey: function listKey() {
    return this.rspNamespace + 's';
  },

  /** The list of fields to expand in resource payloads. */
  expandedFields: [],

  /**
   * Extra query arguments for GET requests.
   *
   * This may also be a function that returns the extra query arguments.
   *
   * These values can be overridden by the caller when making a request.
   * They function as defaults for the queries.
   */
  extraQueryArgs: {},

  /** Whether or not extra data can be associated on the resource. */
  supportsExtraData: false,

  /**
   * A map of attribute names to resulting JSON field names.
   *
   * This is used to auto-generate a JSON payload from attribute names
   * in toJSON().
   *
   * It's also needed if using attribute names in any save({attrs: [...]})
   * calls.
   */
  attrToJsonMap: {},

  /** A list of attributes to serialize in toJSON(). */
  serializedAttrs: [],

  /** A list of attributes to deserialize in parseResourceData(). */
  deserializedAttrs: [],

  /** Special serializer functions called in toJSON(). */
  serializers: {},

  /** Special deserializer functions called in parseResourceData(). */
  deserializers: {},

  /**
   * Initialize the model.
   */
  initialize: function initialize() {
    if (this.supportsExtraData) {
      this._setupExtraData();
    }
  },

  /**
   * Return the URL for this resource's instance.
   *
   * If this resource is loaded and has a URL to itself, that URL will
   * be returned. If not yet loaded, it'll try to get it from its parent
   * object, if any.
   *
   * Returns:
   *     string:
   *     The URL to use when fetching the resource. If the URL cannot be
   *     determined, this will return null.
   */
  url: function url() {
    var links = this.get('links');

    if (links) {
      return links.self.href;
    }

    var parentObject = this.get('parentObject');

    if (parentObject) {
      links = parentObject.get('links');

      if (links) {
        var key = _.result(this, 'listKey');

        var link = links[key];

        if (link) {
          var baseURL = link.href;
          return this.isNew() ? baseURL : baseURL + this.get(this.urlIDAttr) + '/';
        }
      }
    }

    return null;
  },

  /**
   * Call a function when the object is ready to use.
   *
   * An object is ready it has an ID and is loaded, or is a new resource.
   *
   * When the object is ready, options.ready() will be called. This may
   * be called immediately, or after one or more round trips to the server.
   *
   * If we fail to load the resource, objects.error() will be called instead.
   *
   * Args:
   *     options (object):
   *         Options for the fetch operation.
   *
   *     context (object):
   *         Context to bind when executing callbacks.
   *
   * Option Args:
   *     ready (function):
   *         Callback function for when the object is ready to use.
   *
   *     error (function):
   *         Callback function for when an error occurs.
   */
  ready: function ready() {
    var options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
    var context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
    var success = _.isFunction(options.ready) ? _.bind(options.ready, context) : undefined;
    var error = _.isFunction(options.error) ? _.bind(options.error, context) : undefined;
    var parentObject = this.get('parentObject');

    if (this.get('loaded')) {
      // We already have data--just call the callbacks
      if (success) {
        success();
      }
    } else if (!this.isNew()) {
      // Fetch data from the server
      this.fetch({
        data: options.data,
        success: success,
        error: error
      });
    } else if (parentObject) {
      /*
       * This is a new object, which means there's nothing to fetch from
       * the server, but we still need to ensure that the parent is loaded
       * in order for it to have valid links.
       */
      parentObject.ready({
        ready: success,
        error: error
      });
    } else if (success) {
      // Fallback for dummy objects.
      success();
    }
  },

  /**
   * Call a function when we know an object exists server-side.
   *
   * This works like ready() in that it's used to delay operating on the
   * resource until we have a server-side representation. Unlike ready(),
   * it will attempt to create it if it doesn't exist first.
   *
   * When the object has been created, or we know it already is,
   * options.success() will be called.
   *
   * If we fail to create the object, options.error() will be called
   * instead.
   *
   * Args:
   *     options (object):
   *         Object with success and error callbacks.
   *
   *     context (object):
   *         Context to bind when executing callbacks.
   */
  ensureCreated: function ensureCreated() {
    var _this = this;

    var options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
    var context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
    this.ready({
      ready: function ready() {
        if (!_this.get('loaded')) {
          _this.save({
            success: _.isFunction(options.success) ? _.bind(options.success, context) : undefined,
            error: _.isFunction(options.error) ? _.bind(options.error, context) : undefined
          });
        } else if (_.isFunction(options.success)) {
          options.success.call(context);
        }
      }
    });
  },

  /**
   * Fetch the object's data from the server.
   *
   * An object must have an ID before it can be fetched. Otherwise,
   * options.error() will be called.
   *
   * If this has a parent resource object, we'll ensure that's ready before
   * fetching this resource.
   *
   * The resource must override the parse() function to determine how
   * the returned resource data is parsed and what data is stored in
   * this object.
   *
   * If we successfully fetch the resource, options.success() will be
   * called.
   *
   * If we fail to fetch the resource, options.error() will be called.
   *
   * Args:
   *     options (object):
   *         Object with success and error callbacks.
   *
   *     context (object):
   *         Context to bind when executing callbacks.
   */
  fetch: function fetch() {
    var _this2 = this;

    var options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
    var context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
    options = _.bindCallbacks(options, context);

    if (this.isNew()) {
      if (_.isFunction(options.error)) {
        options.error.call(context, 'fetch cannot be used on a resource without an ID');
      }

      return;
    }

    var parentObject = this.get('parentObject');

    if (parentObject) {
      parentObject.ready({
        ready: function ready() {
          return Backbone.Model.prototype.fetch.call(_this2, options);
        },
        error: options.error
      }, this);
    } else {
      Backbone.Model.prototype.fetch.call(this, options);
    }
  },

  /**
   * Save the object's data to the server.
   *
   * If the object has an ID already, it will be saved to its known
   * URL using HTTP PUT. If it doesn't have an ID, it will be saved
   * to its parent list resource using HTTP POST
   *
   * If this has a parent resource object, we'll ensure that's created
   * before saving this resource.
   *
   * An object must either be loaded or have a parent resource linking to
   * this object's list resource URL for an object to be saved.
   *
   * The resource must override the toJSON() function to determine what
   * data is saved to the server.
   *
   * If we successfully save the resource, options.success() will be
   * called, and the "saved" event will be triggered.
   *
   * If we fail to save the resource, options.error() will be called.
   *
   * Args:
   *     options (object):
   *         Object with success and error callbacks.
   *
   *     context (object):
   *         Context to bind when executing callbacks.
   */
  save: function save() {
    var _this3 = this;

    var options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
    var context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
    this.trigger('saving', options);
    this.ready({
      ready: function ready() {
        var parentObject = _this3.get('parentObject');

        if (parentObject) {
          parentObject.ensureCreated({
            success: _this3._saveObject.bind(_this3, options, context),
            error: options.error
          }, _this3);
        } else {
          _this3._saveObject(options, context);
        }
      },
      error: _.isFunction(options.error) ? _.bind(options.error, context) : undefined
    }, this);
  },

  /**
   * Handle the actual saving of the object's state.
   *
   * This is called internally by save() once we've handled all the
   * readiness and creation checks of this object and its parent.
   *
   * Args:
   *     options (object):
   *         Object with success and error callbacks.
   *
   *     context (object):
   *         Context to bind when executing callbacks.
   */
  _saveObject: function _saveObject(options, context) {
    var _this4 = this;

    var url = _.result(this, 'url');

    if (!url) {
      if (_.isFunction(options.error)) {
        options.error.call(context, 'The object must either be loaded from the server or ' + 'have a parent object before it can be saved');
      }

      return;
    }

    var saveOptions = _.defaults({
      success: function success() {
        if (_.isFunction(options.success)) {
          for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
            args[_key] = arguments[_key];
          }

          options.success.apply(context, args);
        }

        _this4.trigger('saved', options);
      },
      error: function error() {
        if (_.isFunction(options.error)) {
          for (var _len2 = arguments.length, args = new Array(_len2), _key2 = 0; _key2 < _len2; _key2++) {
            args[_key2] = arguments[_key2];
          }

          options.error.apply(context, args);
        }

        _this4.trigger('saveFailed', options);
      }
    }, options);

    saveOptions.attrs = options.attrs || this.toJSON(options);
    var files = [];
    var readers = [];

    if (!options.form) {
      if (this.payloadFileKeys && window.File) {
        /* See if there are files in the attributes we're using. */
        this.payloadFileKeys.forEach(function (key) {
          var file = saveOptions.attrs[key];

          if (file) {
            files.push(file);
          }
        });
      }
    }

    if (files.length > 0) {
      files.forEach(function (file) {
        var reader = new FileReader();
        readers.push(reader);

        reader.onloadend = function () {
          if (readers.every(function (r) {
            return r.readyState === FileReader.DONE;
          })) {
            _this4._saveWithFiles(files, readers, saveOptions);
          }
        };

        reader.readAsArrayBuffer(file);
      });
    } else {
      Backbone.Model.prototype.save.call(this, {}, saveOptions);
    }
  },

  /**
   * Save the model with a file upload.
   *
   * When doing file uploads, we need to hand-structure a form-data payload
   * to the server. It will contain the file contents and the attributes
   * we're saving. We can then call the standard save function with this
   * payload as our data.
   *
   * Args:
   *     files (Array of object):
   *         A list of files, with ``name`` and ``type`` keys.
   *
   *     fileReaders (Array of FileReader):
   *         Readers corresponding to each item in ``files``.
   *
   *     options (object):
   *         Options for the save operation.
   *
   * Option Args:
   *     boundary (string):
   *         Optional MIME multipart boundary.
   *
   *     attrs (object):
   *         Additional key/value pairs to include in the payload data.
   */
  _saveWithFiles: function _saveWithFiles(files, fileReaders, options) {
    var boundary = options.boundary || '-----multipartformboundary' + new Date().getTime();
    var blob = [];

    var _iterator = _createForOfIteratorHelper(_.zip(this.payloadFileKeys, files, fileReaders)),
        _step;

    try {
      for (_iterator.s(); !(_step = _iterator.n()).done;) {
        var _step$value = _slicedToArray(_step.value, 3),
            _key3 = _step$value[0],
            file = _step$value[1],
            reader = _step$value[2];

        if (!file || !reader) {
          continue;
        }

        blob.push('--' + boundary + '\r\n');
        blob.push('Content-Disposition: form-data; name="' + _key3 + '"; filename="' + file.name + '"\r\n');
        blob.push('Content-Type: ' + file.type + '\r\n');
        blob.push('\r\n');
        blob.push(reader.result);
        blob.push('\r\n');
      }
    } catch (err) {
      _iterator.e(err);
    } finally {
      _iterator.f();
    }

    for (var _i = 0, _Object$entries = Object.entries(options.attrs); _i < _Object$entries.length; _i++) {
      var _Object$entries$_i = _slicedToArray(_Object$entries[_i], 2),
          key = _Object$entries$_i[0],
          value = _Object$entries$_i[1];

      if (!this.payloadFileKeys.includes(key) && value !== undefined && value !== null) {
        blob.push('--' + boundary + '\r\n');
        blob.push('Content-Disposition: form-data; name="' + key + '"\r\n');
        blob.push('\r\n');
        blob.push(value + '\r\n');
      }
    }

    blob.push('--' + boundary + '--\r\n\r\n');
    Backbone.Model.prototype.save.call(this, {}, _.extend({
      data: new Blob(blob),
      processData: false,
      contentType: 'multipart/form-data; boundary=' + boundary
    }, options));
  },

  /**
   * Delete the object's resource on the server.
   *
   * An object must either be loaded or have a parent resource linking to
   * this object's list resource URL for an object to be deleted.
   *
   * Args:
   *     options (object):
   *         Object with success and error callbacks.
   *
   *     context (object):
   *         Context to bind when executing callbacks.
   */
  destroy: function destroy() {
    var _this5 = this;

    var options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
    var context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : undefined;
    options = _.bindCallbacks(options, context);
    this.trigger('destroying', options);
    var parentObject = this.get('parentObject');

    if (!this.isNew() && parentObject) {
      /*
       * XXX This is temporary to support older-style resource
       *     objects. We should just use ready() once we're moved
       *     entirely onto BaseResource.
       */
      parentObject.ready(_.defaults({
        ready: function ready() {
          return _this5._destroyObject(options, context);
        }
      }, options));
    } else {
      this._destroyObject(options, context);
    }
  },

  /**
   * Set up the deletion of the object.
   *
   * This is called internally by destroy() once we've handled all the
   * readiness and creation checks of this object and its parent.
   *
   * Once we've done some work to ensure the URL is valid and the object
   * is ready, we'll finish destruction by calling _finishDestroy.
   *
   * Args:
   *     options (object):
   *         Object with success and error callbacks.
   *
   *     context (object):
   *         Context to bind when executing callbacks.
   */
  _destroyObject: function _destroyObject() {
    var _this6 = this;

    var options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
    var context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : null;

    var url = _.result(this, 'url');

    if (!url) {
      if (this.isNew()) {
        /*
         * If both this resource and its parent are new, it's possible
         * that we'll get through here without a url. In this case, all
         * the data is still local to the client and there's not much to
         * clean up; just call Model.destroy and be done with it.
         */
        this._finishDestroy(options, context);
      } else if (_.isFunction(options.error)) {
        options.error.call(context, 'The object must either be loaded from the server or ' + 'have a parent object before it can be deleted');
      }

      return;
    }

    this.ready({
      ready: function ready() {
        return _this6._finishDestroy(options, context);
      },
      error: _.isFunction(options.error) ? _.bind(options.error, context) : undefined
    }, this);
  },

  /**
   * Finish destruction of the object.
   *
   * This will call the parent destroy method, then reset the state
   * of the object on success.
   *
   * Args:
   *     options (object):
   *         Object with success and error callbacks.
   *
   *     context (object):
   *         Context to bind when executing callbacks.
   */
  _finishDestroy: function _finishDestroy(options, context) {
    var _this7 = this;

    var parentObject = this.get('parentObject');
    Backbone.Model.prototype.destroy.call(this, _.defaults({
      wait: true,
      success: function success() {
        /*
         * Reset the object so it's new again, but with the same
         * parentObject.
         */
        _this7.set(_.defaults({
          id: null,
          parentObject: parentObject
        }, _.result(_this7, 'defaults')));

        _this7.trigger('destroyed', options);

        if (_.isFunction(options.success)) {
          for (var _len3 = arguments.length, args = new Array(_len3), _key4 = 0; _key4 < _len3; _key4++) {
            args[_key4] = arguments[_key4];
          }

          options.success.apply(context, args);
        }
      }
    }, _.bindCallbacks(options, context)));
  },

  /**
   * Parse and returns the payload from an API response.
   *
   * This will by default only return the object's ID and list of links.
   * Subclasses should override this to return any additional data that's
   * needed, but they must include the results of
   * BaseResource.protoype.parse as well.
   *
   * Args:
   *     rsp (object):
   *         The payload received from the server.
   *
   * Returns:
   *     object:
   *     Attributes to set on the model.
   */
  parse: function parse(rsp) {
    console.assert(this.rspNamespace, 'rspNamespace must be defined on the resource model');

    if (rsp.stat !== undefined) {
      /*
       * This resource payload is inside an envelope from an API
       * call. It's not model construction data or from a list
       * resource.
       */
      rsp = rsp[this.rspNamespace];
    }

    return _.defaults({
      extraData: rsp.extra_data,
      id: rsp.id,
      links: rsp.links,
      loaded: true
    }, this.parseResourceData(rsp));
  },

  /*
   * Parse the resource data from a payload.
   *
   * By default, this will make use of attrToJsonMap and any
   * jsonDeserializers to construct a resulting set of attributes.
   *
   * This can be overridden by subclasses.
   *
   * Args:
   *     rsp (object):
   *         The payload received from the server.
   *
   * Returns:
   *     object:
   *     Attributes to set on the model.
   */
  parseResourceData: function parseResourceData(rsp) {
    var attrs = {};

    var _iterator2 = _createForOfIteratorHelper(this.deserializedAttrs),
        _step2;

    try {
      for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
        var attrName = _step2.value;
        var deserializer = this.deserializers[attrName];
        var jsonField = this.attrToJsonMap[attrName] || attrName;
        var value = rsp[jsonField];

        if (deserializer) {
          value = deserializer.call(this, value);
        }

        if (value !== undefined) {
          attrs[attrName] = value;
        }
      }
    } catch (err) {
      _iterator2.e(err);
    } finally {
      _iterator2.f();
    }

    return attrs;
  },

  /**
   * Serialize and return object data for the purpose of saving.
   *
   * When saving to the server, the only data that will be sent in the
   * API PUT/POST call will be the data returned from toJSON().
   *
   * This will build the list based on the serializedAttrs, serializers,
   * and attrToJsonMap properties.
   *
   * Subclasses can override this to create custom serialization behavior.
   *
   * Returns:
   *     object:
   *     The serialized data.
   */
  toJSON: function toJSON() {
    var serializerState = {
      isNew: this.isNew(),
      loaded: this.get('loaded')
    };
    var data = {};

    var _iterator3 = _createForOfIteratorHelper(this.serializedAttrs),
        _step3;

    try {
      for (_iterator3.s(); !(_step3 = _iterator3.n()).done;) {
        var attrName = _step3.value;
        var serializer = this.serializers[attrName];
        var value = this.get(attrName);

        if (serializer) {
          value = serializer.call(this, value, serializerState);
        }

        var jsonField = this.attrToJsonMap[attrName] || attrName;
        data[jsonField] = value;
      }
    } catch (err) {
      _iterator3.e(err);
    } finally {
      _iterator3.f();
    }

    if (this.supportsExtraData) {
      _.extend(data, this.extraData.toJSON());
    }

    return data;
  },

  /**
   * Handle all AJAX communication for the model and its subclasses.
   *
   * Backbone.js will internally call the model's sync function to
   * communicate with the server, which usually uses Backbone.sync.
   *
   * We wrap this to convert the data to encoded form data (instead
   * of Backbone's default JSON payload).
   *
   * We also parse the error response from Review Board so we can provide
   * a more meaningful error callback.
   *
   * Args:
   *     method (string):
   *         The HTTP method to use.
   *
   *     model (Backbone.Model):
   *         The model to sync.
   *
   *     options (object):
   *         Options for the operation.
   *
   * Option Args:
   *     data (object):
   *         Optional payload data to include.
   *
   *     form (jQuery):
   *         Optional form to be submitted.
   *
   *     attrs (Array or object):
   *         Either a list of the model attributes to sync, or a set of
   *         key/value pairs to use instead of the model attributes.
   */
  sync: function sync(method, model) {
    var _this8 = this;

    var options = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : {};
    var data;
    var contentType;

    if (method === 'read') {
      data = options.data || {};

      var extraQueryArgs = _.result(this, 'extraQueryArgs', {});

      if (!_.isEmpty(extraQueryArgs)) {
        data = _.extend({}, extraQueryArgs, data);
      }
    } else {
      if (options.form) {
        data = null;
      } else if (options.attrs && !_.isArray(options.attrs)) {
        data = options.attrs;
      } else {
        data = model.toJSON(options);

        if (options.attrs) {
          data = _.pick(data, options.attrs.map(function (attr) {
            return _this8.attrToJsonMap[attr] || attr;
          }));
        }
      }

      contentType = 'application/x-www-form-urlencoded';
    }

    var syncOptions = _.defaults({}, options, {
      /* Use form data instead of a JSON payload. */
      contentType: contentType,
      data: data,
      processData: true
    });

    if (!options.form && this.expandedFields.length > 0) {
      syncOptions.data.expand = this.expandedFields.join(',');
    }

    syncOptions.error = function (xhr) {
      RB.storeAPIError(xhr);
      var rsp = xhr.errorPayload;

      if (rsp && _.has(rsp, _this8.rspNamespace)) {
        /*
         * The response contains the current version of the object,
         * which we want to preserve, in case it did any partial
         * updating of data.
         */
        _this8.set(_this8.parse(rsp));
      }

      if (_.isFunction(options.error)) {
        options.error(xhr);
      }
    };

    return Backbone.sync.call(this, method, model, syncOptions);
  },

  /**
   * Perform validation on the attributes of the resource.
   *
   * By default, this validates the extraData field, if provided.
   *
   * Args:
   *     attrs (object):
   *         The attributes to validate.
   *
   * Returns:
   *     string:
   *     An error string or ``undefined``.
   */
  validate: function validate(attrs) {
    if (this.supportsExtraData && attrs.extraData !== undefined) {
      var strings = RB.BaseResource.strings;

      if (!_.isObject(attrs.extraData)) {
        return strings.INVALID_EXTRADATA_TYPE;
      }

      for (var _i2 = 0, _Object$entries2 = Object.entries(attrs.extraData); _i2 < _Object$entries2.length; _i2++) {
        var _Object$entries2$_i = _slicedToArray(_Object$entries2[_i2], 2),
            key = _Object$entries2$_i[0],
            value = _Object$entries2$_i[1];

        if (!_.isNull(value) && (!_.isNumber(value) || _.isNaN(value)) && !_.isBoolean(value) && !_.isString(value)) {
          return strings.INVALID_EXTRADATA_VALUE_TYPE.replace('{key}', key);
        }
      }
    }
  }
}, {
  strings: {
    UNSET_PARENT_OBJECT: 'parentObject must be set',
    INVALID_EXTRADATA_TYPE: 'extraData must be an object or undefined',
    INVALID_EXTRADATA_VALUE_TYPE: 'extraData.{key} must be null, a number, boolean, or string'
  }
});

_.extend(RB.BaseResource.prototype, RB.ExtraDataMixin);

//# sourceMappingURL=baseResourceModel.js.map