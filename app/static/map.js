//Variables
const markerSRC = "../static/images/marker.png";

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

//DRAW MARKERS--
for (let i = 0; i < locations.length; i++) { //for every location in list

    const marker = new ol.Feature({ //create a marker variable
        geometry: new ol.geom.Point(
            ol.proj.fromLonLat(locations[i])
        ),
    });
    marker.setStyle(new ol.style.Style({ //style with a png
        image: new ol.style.Icon(({
            src: markerSRC,
        }))
    }));
    const vectorSource = new ol.source.Vector({ //create a source from the marker
        features: [marker]
    });
    const markerVectorLayer = new ol.layer.Vector({ //create a layer from the source
        source: vectorSource,
    });

    map.addLayer(markerVectorLayer); //add layer to map
}
//DRAW