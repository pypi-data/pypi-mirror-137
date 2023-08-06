"use strict";

suite('rb/newReviewRequest/views/RepositorySelectionView', function () {
  var collection;
  var view;
  beforeEach(function () {
    collection = new Backbone.Collection([{
      name: 'Bitbucket Test'
    }, {
      name: 'GitHub Test'
    }, {
      name: 'GitLab Test'
    }, {
      name: 'Local Git Test'
    }], {
      model: RB.Repository
    });
    view = new RB.RepositorySelectionView({
      collection: collection
    });
  });
  describe('Rendering', function () {
    it('With items', function () {
      view.render();
      var children = view.$el.find('.repository');
      expect(children.length).toBe(collection.models.length);

      for (var i = 0; i < children.length; i++) {
        var name = collection.models[i].get('name');
        expect($(children[i]).text().strip()).toBe(name);
      }
    });
  });
  describe('Filtering', function () {
    var $items;
    var $searchBox;

    function setSearchTerm(term) {
      $searchBox.val(term).trigger('input');
    }

    function checkVisibility(i, visible) {
      expect($items.eq(i).is(':visible')).toBe(visible);
    }

    beforeEach(function () {
      view.render().$el.appendTo($testsScratch);
      $items = view.$el.find('.repository');
      $searchBox = view.$el.find('.rb-c-search-field__input');
      expect($items.length).toBe(4);
      expect($searchBox.length).toBe(1);
    });
    it('No search term', function () {
      $items.each(function (i, el) {
        checkVisibility(i, true);
      });
    });
    it('Search term set and match', function () {
      setSearchTerm('Git');
      checkVisibility(0, false);
      checkVisibility(1, true);
      checkVisibility(2, true);
      checkVisibility(3, true);
    });
    it('Search term set and no match', function () {
      setSearchTerm('XXX');
      $items.each(function (i, el) {
        checkVisibility(i, false);
      });
    });
    it('Search term removed', function () {
      setSearchTerm('Git');
      checkVisibility(0, false);
      checkVisibility(1, true);
      checkVisibility(2, true);
      checkVisibility(3, true);
      setSearchTerm('');
      $items.each(function (i, el) {
        checkVisibility(i, true);
      });
    });
  });
  describe('Selected event', function () {
    it('When clicked', function () {
      var handlerCalled = false;
      view.render();
      view.on('selected', function (repository) {
        expect(repository.get('name')).toBe('GitHub Test');
        handlerCalled = true;
      });
      var children = view.$el.find('.repository');
      $(children[1]).click();
      expect(handlerCalled).toBe(true);
    });
  });
});

//# sourceMappingURL=repositorySelectionViewTests.js.map