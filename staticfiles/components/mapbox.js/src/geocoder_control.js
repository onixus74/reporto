'use strict';

var geocoder = require('./geocoder');

var GeocoderControl = L.Control.extend({
    includes: L.Mixin.Events,

    initialize: function(_) {
        this.geocoder = geocoder(_);
    },

    setURL: function(_) {
        this.geocoder.setURL(_);
        return this;
    },

    getURL: function() {
        return this.geocoder.getURL();
    },

    setID: function(_) {
        this.geocoder.setID(_);
        return this;
    },

    setTileJSON: function(_) {
        this.geocoder.setTileJSON(_);
        return this;
    },

    onAdd: function(map) {
        this._map = map;

        var className = 'leaflet-control-mapbox-geocoder',
            container = L.DomUtil.create('div', className);

        L.DomEvent.disableClickPropagation(container);

        var form = this._form = L.DomUtil.create('form', className + '-form');
        L.DomEvent.addListener(form, 'submit', this._geocode, this);

        var input = this._input = document.createElement('input');
        input.type = 'text';

        var submit = this._submit = document.createElement('input');
        submit.type = 'submit';
        submit.className = 'mapbox-button';
        submit.value = 'Locate';

        form.appendChild(input);
        form.appendChild(submit);
        container.appendChild(form);

        return container;
    },

    _geocode: function(event) {
        L.DomEvent.preventDefault(event);
        L.DomUtil.addClass(this._container, 'searching');
        this.geocoder.query(this._input.value, L.bind(function(err, res) {
            L.DomUtil.removeClass(this._container, 'searching');
            if (err) {
                this.fire('error', {error: err});
            } else {
                if (res.lbounds) this._map.fitBounds(res.lbounds);
                else this._map.setView(res.latlng, 6);
                this.fire('found', res);
            }
        }, this));
    }
});

module.exports = function(options) {
    return new GeocoderControl(options);
};
