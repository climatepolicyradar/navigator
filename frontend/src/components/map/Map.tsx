import Script from "next/script";
import Head from "next/head";
import { MapContainer, Marker, Popup, TileLayer, Polygon, GeoJSON } from "react-leaflet";
import GeoJsonData from "../../../public/data/geojson/world.geo.json";

const geoOptions = { color: "purple" };

type TGeo = {
  type: string;
  properties: { adm0_a3: string };
  geometry: {
    type: string;
    coordinates: [number, number][];
  };
};

const Map = () => {
  const data: any = GeoJsonData;

  // function to calculate the center of the polygon
  const getCenter = (coordinates: [number, number][]) => {
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

  const myCustomStyle = {
    stroke: true,
    color: "#000",
    opacity: 0.4,
    dashArray: "5, 5",
    strokeStyle: "dash",
    fill: true,
    fillColor: "#fff",
    fillOpacity: 0,
  };

  return (
    <>
      <Head>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css" integrity="sha256-kLaT2GOSpHechhsozzB+flnD+zUyjE2LlfWPgU04xyI=" crossOrigin="" />
      </Head>
      <Script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js" integrity="sha256-WBkoXOwTeyKclOHuWtc+i2uENFpDZ9YPdf5Hf+D7ewM=" crossOrigin=""></Script>
      <div style={{ aspectRatio: (1000 / 400).toString() }}>
        <MapContainer center={[51.505, -0.09]} zoom={3} minZoom={2} scrollWheelZoom={false} className="h-full w-full">
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          <GeoJSON data={data} style={myCustomStyle} />
        </MapContainer>
      </div>
    </>
  );
};

export default Map;
