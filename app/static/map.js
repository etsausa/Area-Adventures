//Variables
const markerSRC ="../static/marker.png";

const giles = [-76.489588, 42.435663];
const park = [-76.494789, 42.424169];
const ithaca = [-76.4955, 42.4395];

const locations = [giles, park, ithaca]; //list of all locations

//CONSTRUCT MAP --
const map = new ol.Map({

    target: 'map',
    layers: [new ol.layer.Tile({
        source: new ol.source.OSM()
    })],
    view: new ol.View({
        center: ol.proj.fromLonLat(ithaca),
        zoom: 13
    })
});

//DRAW MARKERS --
for (let i = 0; i < locations.length; i++) { //for every location in list

    const markerFeature = new ol.Feature({ //create a marker variable
        geometry: new ol.geom.Point(
            ol.proj.fromLonLat(locations[i]),
        ),
        name: "location " + locations[i],
    });
    markerFeature.setStyle(new ol.style.Style({ //style with a png
        image: new ol.style.Icon(({
            src: markerSRC,
        }))
    }));
    const vectorSource = new ol.source.Vector({ //create a source from the marker
        features: [markerFeature]
    });
    const markerVectorLayer = new ol.layer.Vector({ //create a layer from the source
        source: vectorSource,
    });

    map.addLayer(markerVectorLayer); //add layer to map
}
//ONCLICK -- this doesnt work but it also doesnt break anything yet
const element = document.getElementById('popup');

const popup = new ol.Overlay({
  element: element,
  positioning: 'bottom-center',
  stopEvent: false,
  offset: [0, -50]
});

map.addOverlay(popup);

// display popup on click
map.on('click', function(evt) {
  const feature = map.forEachFeatureAtPixel(evt.pixel,
    function(feature) {
      return feature;
    });
  if (feature) {
    const coordinates = feature.getGeometry().getCoordinates();
    popup.setPosition(coordinates);
    $(element).popover({
      placement: 'top',
      html: true,
      content: feature.get('name')
    });
    $(element).popover('show');
  } else {
    $(element).popover('destroy');
  }
});

// change mouse cursor when over marker
map.on('pointermove', function(e) {
  if (e.dragging) {
    $(element).popover('destroy');
    return;
  }
  const pixel = map.getEventPixel(e.originalEvent);
  const hit = map.hasFeatureAtPixel(pixel);
  map.getTarget().style.cursor = hit ? 'pointer' : '';
});


//example links:
//https://openlayers.org/en/latest/examples/hit-tolerance.html
//https://openlayers.org/en/latest/examples/select-hover-features.html
//https://openlayers.org/en/latest/examples/icon.html?q=pop+up

