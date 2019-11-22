//Variables
const markerSRC ="../static/marker.png";

const giles = [-76.489588, 42.435663];
const park = [-76.494789, 42.424169];
const ithaca = [-76.4955, 42.4395];

const locations = [giles, park, ithaca]; //list of all locations
const startingLoc = ithaca;

//CONSTRUCT MAP --

const layer01 = new ol.layer.Tile({
        source: new ol.source.OSM()
    })

const view01 = new ol.View({ //view
        center: ol.proj.fromLonLat(startingLoc),
        zoom: 13
    })

const map = new ol.Map({

    target: document.getElementById('map'),
    layers: [layer01],
    view: view01
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


//example links:
//https://openlayers.org/en/latest/examples/hit-tolerance.html
//https://openlayers.org/en/latest/examples/select-hover-features.html
//https://openlayers.org/en/latest/examples/icon.html?q=pop+up

