"use strict";

/**
 * A view for managing the administration UI's database model change pages.
 *
 * This sets up the page to manage the configuration form and any inline
 * groups used for adding, modifying, or deleting related objects.
 */
RB.Admin.ChangeFormPageView = RB.Admin.PageView.extend({
  /**
   * Initialize the view.
   *
   * Args:
   *     options (object):
   *         The options passed to the page.
   *
   * Option Args:
   *     formID (string):
   *         The element ID for the form.
   */
  initialize: function initialize(options) {
    RB.Admin.PageView.prototype.initialize.call(this, options);
    this.formID = options.formID;
    this.formView = null;
    this.inlineGroupViews = [];
  },

  /**
   * Render the page.
   *
   * This will set up the form and inline group management.
   */
  renderPage: function renderPage() {
    var _this = this;

    RB.Admin.PageView.prototype.renderPage.call(this);
    console.assert(this.inlineGroupViews.length === 0);
    this.formView = new RB.FormView({
      el: $("#".concat(this.formID))
    });
    this.formView.render();
    this.$('.rb-c-admin-form-inline-group').each(function (i, el) {
      var inlineGroup = new RB.Admin.InlineFormGroup({
        prefix: $(el).data('prefix')
      });
      var inlineGroupView = new RB.Admin.InlineFormGroupView({
        el: el,
        model: inlineGroup
      });
      inlineGroupView.renderPage();

      _this.inlineGroupViews.push(inlineGroupView);

      _this.listenTo(inlineGroupView, 'inlineFormAdded', function () {
        return _this.formView.setupFormWidgets(inlineGroupView.$el);
      });
    });
  }
});

//# sourceMappingURL=changeFormPageView.js.map