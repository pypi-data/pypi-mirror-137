"use strict";

/**
 * A view that allows users to select a revision of a file attachment to view.
 */
RB.FileAttachmentRevisionSelectorView = RB.RevisionSelectorView.extend({
  /**
   * Initialize the view.
   */
  initialize: function initialize() {
    RB.RevisionSelectorView.prototype.initialize.call(this, {
      firstLabelActive: true,
      numHandles: 2
    });
  },

  /**
   * Render the view.
   *
   * Returns:
   *     RB.FileAttachmentRevisionSelectorView:
   *     This object, for chaining.
   */
  render: function render() {
    var numRevisions = this.model.get('numRevisions');
    var labels = [gettext("No Diff")];

    for (var i = 1; i <= numRevisions; i++) {
      labels.push(i.toString());
    }

    RB.RevisionSelectorView.prototype.render.call(this, labels, true
    /* whether the first label is clickable */
    );
  },

  /**
   * Update the displayed revision based on the model.
   */
  _update: function _update() {
    var revision = this.model.get('fileRevision');
    var diffRevision = this.model.get('diffRevision');

    if (diffRevision) {
      this._values = [revision, diffRevision];
    } else {
      this._values = [0, revision];
    }

    if (this._rendered) {
      this._updateHandles();
    }
  },

  /**
   * Callback for when one of the labels is clicked.
   *
   * This will jump to the target revision.
   *
   * Args:
   *     ev (Event):
   *         The click event.
   */
  _onLabelClick: function _onLabelClick(ev) {
    var $target = $(ev.currentTarget);
    this.trigger('revisionSelected', [0, $target.data('revision')]);
  }
});

//# sourceMappingURL=fileAttachmentRevisionSelectorView.js.map