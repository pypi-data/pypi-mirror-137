"use strict";

function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

function _iterableToArrayLimit(arr, i) { var _i = arr == null ? null : typeof Symbol !== "undefined" && arr[Symbol.iterator] || arr["@@iterator"]; if (_i == null) return; var _arr = []; var _n = true; var _d = false; var _s, _e; try { for (_i = _i.call(arr); !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

(function () {
  var addApplicationText = gettext("Add application");
  var disabledForSecurityText = gettext("Disabled for security.");
  var disabledWarningTemplate = gettext("This application has been disabled because the user \"%s\" has been removed from the Local Site.");
  var emptyText = gettext("You have not registered any OAuth2 applications.");
  var localSiteEmptyText = gettext("You have not registered any OAuth2 applications on %s.");
  /**
   * A model representing an OAuth application.
   *
   * Model Attributes:
   *     apiURL (string):
   *         The URL to the application list reosurce.
   *
   *     enabled (boolean):
   *         Whether or not the application is enabled.
   *
   *     editURL (string):
   *         The URL to edit this application.
   *
   *     isDisabledForSecurity (bool):
   *         When true, this attribute indicates that the application was
   *         re-assigned to the current user because the original user was
   *         removed from the Local Site associated with this.
   *
   *     localSiteName (string):
   *         The name of the LocalSite the application is restricted to.
  
   *     name (string):
   *         The name of the application.
   *
   *     originalUser (string):
   *         The username of the user who originally owned this application. This
   *         will only be set if :js:attr:`enabled` is ``false``.
   *
   *     showRemove (boolean):
   *         Whether or not the "Remove Item" link should be shown.
   *
   *         This is always true.
   */

  var OAuthAppItem = Djblets.Config.ListItem.extend({
    defaults: _.defaults({
      apiURL: '',
      editURL: '',
      enabled: true,
      isDisabledForSecurity: false,
      localSiteName: '',
      name: '',
      originalUser: null,
      showRemove: true
    }, Djblets.Config.ListItem.prototype.defaults),

    /**
     * Parse a raw object into the properties of an OAuthAppItem.
     *
     * Args:
     *     rsp (object):
     *         The raw properties of the item.
     *
     *     options (object):
     *         Options for generating properties.
     *
     *         The values in this object will be used to generate the ``apiUrl``
     *         and ``editURL`` properties.
     *
     * Option Args:
     *     baseURL (string):
     *         The base API URL for the object.
     *
     *     baseEditURL (string):
     *         The base URL for the edit view.
     *
     * Returns:
     *     object:
     *     An object containing the properties of an OAuthAppItem.
     */
    parse: function parse(rsp, options) {
      var baseEditURL = options.baseEditURL,
          baseURL = options.baseURL;
      var localSiteName = rsp.localSiteName;
      return _.defaults(rsp, {
        apiURL: localSiteName ? "/s/".concat(localSiteName).concat(baseURL).concat(rsp.id, "/") : "".concat(baseURL).concat(rsp.id, "/"),
        editURL: "".concat(baseEditURL, "/").concat(rsp.id, "/")
      });
    }
  });
  /**
   * A view corresponding to a single OAuth2 application.
   */

  var OAuthAppItemView = Djblets.Config.ListItemView.extend({
    template: _.template("<div class=\"app-entry-wrapper\">\n <span class=\"config-app-name<% if (!enabled) {%> disabled<% } %>\">\n  <% if (isDisabledForSecurity) { %>\n    <span class=\"rb-icon rb-icon-warning\"\n          title=\"".concat(disabledForSecurityText, "\"></span>\n  <% } %>\n  <a href=\"<%- editURL %>\"><%- name %></a>\n </span>\n <% if (isDisabledForSecurity) { %>\n   <p class=\"disabled-warning\"><%- disabledWarning %></p>\n  <% } %>\n </div>")),
    actionHandlers: {
      'delete': '_onDeleteClicked'
    },

    /**
     * Return additional rendering context.
     *
     * Returns:
     *     object:
     *     Additional rendering context.
     */
    getRenderContext: function getRenderContext() {
      return {
        disabledWarning: interpolate(disabledWarningTemplate, [this.model.get('originalUser')])
      };
    },

    /**
     * Delete the OAuth2 application.
     */
    _onDeleteClicked: function _onDeleteClicked() {
      var _this = this;

      RB.apiCall({
        url: this.model.get('apiURL'),
        method: 'DELETE',
        success: function success() {
          return _this.model.trigger('destroy');
        },
        error: function error(xhr) {
          return alert(xhr.errorText);
        }
      });
    }
  });
  /**
   * A view for managing the user's OAuth2 applications.
   */

  RB.OAuthApplicationsView = Backbone.View.extend({
    template: _.template("<div class=\"app-lists\"></div>\n<div class=\"oauth-form-buttons djblets-l-config-forms-container\">\n <a class=\"btn oauth-add-app\" href=\"<%- editURL %>\">\n  ".concat(addApplicationText, "\n </a>\n</div>")),
    listTemplate: _.template("<div>\n <% if (localSiteName) { %>\n  <div class=\"djblets-l-config-forms-container\">\n   <h2><%- localSiteName %></h2>\n  </div>\n <% } %>\n <div class=\"app-list\">\n  <div class=\"djblets-l-config-forms-container\">\n   <%- emptyText %>\n  </div>\n </div>\n</div>"),

    /**
     * Initialize the view.
     *
     * Args:
     *     options (object):
     *         View options.
     *
     * Option Args:
     *     apps (array):
     *         The array of serialized application information.
     *
     *     addText (string):
     *         The localized text for adding an option.
     *
     *     editURL (string):
     *         The URL of the "edit-oauth-app" view.
     *
     *     emptyText (string):
     *         The localized text for indicating there are no applications.
     */
    initialize: function initialize(options) {
      this.collections = new Map(Object.entries(options.apps).map(function (_ref) {
        var _ref2 = _slicedToArray(_ref, 2),
            localSiteName = _ref2[0],
            apps = _ref2[1];

        return [localSiteName || null, new Backbone.Collection(apps, {
          model: OAuthAppItem,
          parse: true,
          baseEditURL: options.editURL,
          baseURL: options.baseURL
        })];
      }));
      this._editURL = options.editURL;
      window.view = this;
    },

    /**
     * Render an application list for the given LocalSite.
     *
     * Args:
     *     localSiteName (string):
     *         The name of the LocalSite or ``null``.
     *
     *     collection (Backbone.Collection):
     *         The collection of models.
     *
     * Returns:
     *     jQuery:
     *     The rendered list.
     */
    _renderAppList: function _renderAppList(localSiteName, collection) {
      var $entry = $(this.listTemplate({
        emptyText: localSiteName ? interpolate(localSiteEmptyText, [localSiteName]) : emptyText,
        localSiteName: localSiteName
      }));
      var listView = new Djblets.Config.ListView({
        ItemView: OAuthAppItemView,
        model: new Djblets.Config.List({}, {
          collection: collection
        })
      });
      listView.render().$el.prependTo($entry.find('.app-list'));
      return $entry;
    },

    /**
     * Render the view.
     *
     * Returns:
     *     RB.OAuthApplicationsView:
     *     This view.
     */
    render: function render() {
      var _this2 = this;

      this.$el.html(this.template({
        editURL: this._editURL
      }));
      var $lists = this.$('.app-lists');
      this.collections.forEach(function (collection, localSiteName) {
        var $entry = _this2._renderAppList(localSiteName, collection);

        if (localSiteName) {
          $lists.append($entry);
        } else {
          $lists.prepend($entry);
        }
      });
      return this;
    }
  });
})();

//# sourceMappingURL=oauthApplicationsView.js.map