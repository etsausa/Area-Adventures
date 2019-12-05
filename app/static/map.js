
//Variables
const markerSRC ="../static/marker.png";

//locations for testing
const giles = [-76.489588, 42.435663];
const park = [-76.494789, 42.424169];
const ithaca = [-76.4955, 42.4395];

const locations = [giles, park, ithaca]; //list of all locations
const names = ["giles", "park", "ithaca"]
const startingLoc = ithaca;


//CONSTRUCT MAP --
const layer01 = new ol.layer.Tile({ //holds map images
    source: new ol.source.OSM() //MAP IMAGES SOURCE
});

const view01 = new ol.View({ //contains data on starting view
    center: ol.proj.fromLonLat(startingLoc),
    zoom: 13
});

const map = new ol.Map({ //creates map
    target: document.getElementById('map'),
    layers: [layer01],
    view: view01,
});

for(let i = 0; i < locations.length; i++) { //for every post

//DRAW MARKER --
    const markerFeature = new ol.Feature({ //create a marker variable
        geometry: new ol.geom.Point(
            ol.proj.fromLonLat(locations[i]),
        ),
        name: names[i],
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
        source: vectorSource
    });

    map.addLayer(markerVectorLayer); //add layer to map


}

//CONSTRUCT OVERLAY
//assign variables to HTML divs
const container = document.getElementById('popup');
const content = document.getElementById('popup-content');
const closer = document.getElementById('popup-closer');

const overlay = new ol.Overlay({ //create overlay
    element: container,
    autoPan: true,
    autoPanAnimation: {
        duration: 250
    }
});
map.addOverlay(overlay);

//CLICK LISTENER
closer.onclick = function () { //creates a button to close popup
    overlay.setPosition(undefined);
    closer.blur();
    return false;
};

map.on('singleclick', function (event) { //create popup on click
    let feature = map.forEachFeatureAtPixel(event.pixel, //at pos clicked, check if there is a feature
        function(feature) {
            return feature;
        });
    if(feature) { //if there is a feature
        let coordinates = feature.getGeometry().getCoordinates();
        overlay.setPosition(coordinates); //draw popup at coords of marker
        content.innerHTML = feature.get('name'); //grab the it's info

    }
});


//example links:
//https://openlayers.org/en/latest/examples/hit-tolerance.html
//https://openlayers.org/en/latest/examples/select-hover-features.html
//https://openlayers.org/en/latest/examples/icon.html?q=pop+up

