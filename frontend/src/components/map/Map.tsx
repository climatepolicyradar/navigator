import { useMemo } from "react";
import Script from "next/script";
import Head from "next/head";
import Leaflet from "leaflet";
import TurfCenter from "@turf/center";
import { AllGeoJSON } from "@turf/helpers";
import { feature, mergeArcs } from "topojson-client";
import { MapContainer, Marker, Popup, TileLayer, Polygon, GeoJSON, CircleMarker } from "react-leaflet";
import GeoJsonData from "../../../public/data/geojson/world.geo.json";
import CCLWData from "../../../public/data/cclw/world.topo.json";
import { geoCentrePoints } from "@constants/mapCentres";

type TGeo = {
  type: string;
  properties: { adm0_a3: string };
  geometry: {
    type: string;
    coordinates: AllGeoJSON;
  };
};

type TGeoCircle = {
  centerCalc: any;
  // country: string;
};

type TGeoCircleM = {
  centerCalc: any;
  // country: string;
};

type TGeoCoords = [number, number][];

// function to calculate the center of the polygon
const getCenter = (coordinates: TGeoCoords): [number, number] => {
  const center = coordinates.reduce(
    (acc, coord) => {
      acc[0] += coord[0];
      acc[1] += coord[1];
      return acc;
    },
    [0, 0]
  );
  return [center[0] / coordinates.length, center[1] / coordinates.length];
};

const generateGeoCircles = (geos: AllGeoJSON[]): TGeoCircle[] => {
  return geos.map((feature: AllGeoJSON) => {
    const centerCalc = TurfCenter(feature);

    return {
      centerCalc,
      // country: feature.properties.adm0_a3,
    };
  });
};

const generateGeoCirclesManually = (geos: TGeo[]): TGeoCircleM[] => {
  console.log(geos);
  return geos.map((feature: TGeo) => {
    const centerCalc = getCenter(feature.geometry.coordinates[0]);

    return {
      centerCalc,
    };
  });
};

const Map = () => {
  // const mapData: any = GeoJsonData;
  // const dataCircles = generateGeoCircles(data.features);
  // const dataCirclesManual = generateGeoCirclesManually(data.features);
  // console.log(dataCircles.map((geoCircle) => geoCircle.center));
  // console.log(data);
  // console.log(dataCircles);
  // console.log(dataCirclesManual);
  const data: any = CCLWData;
  const mapData = feature(data, CCLWData.objects[Object.keys(data.objects)[0]]);
  // console.log(mapData);
  const geoCentres: any = geoCentrePoints;
  // console.log(geoCentres);

  const geoClickHandler = (e: any) => {
    return false;
    // console.log(e);
  };

  const myCustomStyle = {
    stroke: true,
    color: "#000",
    opacity: 0.4,
    fill: true,
    fillColor: "#fff",
    fillOpacity: 1,
  };

  const geoEventHandlers = {
    click: geoClickHandler,
  };

  return (
    <>
      <Head>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css" integrity="sha256-kLaT2GOSpHechhsozzB+flnD+zUyjE2LlfWPgU04xyI=" crossOrigin="" />
      </Head>
      <Script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js" integrity="sha256-WBkoXOwTeyKclOHuWtc+i2uENFpDZ9YPdf5Hf+D7ewM=" crossOrigin=""></Script>
      <div style={{ aspectRatio: (1000 / 400).toString() }}>
        <MapContainer center={[51.505, -0.09]} zoom={3} minZoom={2} scrollWheelZoom={false} className="h-full w-full">
          {/* <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" /> */}
          {/* <GeoJSON data={data} style={myCustomStyle} eventHandlers={geoEventHandlers} />
          {dataCircles &&
            dataCircles.map((geoCircle, i) => {
              // if (Number.isNaN(geoCircle.center[0]) || Number.isNaN(geoCircle.center[1])) return null;
              return <CircleMarker key={i} center={geoCircle.centerCalc.geometry.coordinates} radius={20} fillOpacity={0.5} stroke={false} eventHandlers={geoEventHandlers} />;
            })}
          {dataCirclesManual &&
            dataCirclesManual.map((geoCircle, i) => {
              if (Number.isNaN(geoCircle.centerCalc[0]) || Number.isNaN(geoCircle.centerCalc[1])) return null;
              return (
                <CircleMarker
                  key={i}
                  center={geoCircle.centerCalc}
                  radius={20}
                  fillOpacity={0.5}
                  stroke={false}
                  color={"red"}
                  eventHandlers={geoEventHandlers}
                />
              );
            })} */}
          <GeoJSON data={mapData} style={myCustomStyle} eventHandlers={geoEventHandlers} />
          {geoCentres &&
            Object.keys(geoCentres).map((ISO, i) => {
              if (Number.isNaN(geoCentres[ISO]) || Number.isNaN(geoCentres[ISO])) return null;
              return (
                <CircleMarker key={i} center={[geoCentres[ISO][1], geoCentres[ISO][0]]} radius={5} fillOpacity={0.5} stroke={false} color={"red"} eventHandlers={geoEventHandlers}>
                  <Popup>{ISO}</Popup>
                </CircleMarker>
              );
            })}
        </MapContainer>
      </div>
    </>
  );
};

export default Map;
