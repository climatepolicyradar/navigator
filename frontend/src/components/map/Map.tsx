import Script from "next/script";
import Head from "next/head";
import { MapContainer, Marker, Popup, TileLayer, Polygon } from "react-leaflet";
import GeoJsonData from "../../../public/data/geojson/world.geo.json";

const geoOptions = { color: "purple" };

type TGeo = {
  type: string;
  properties: { adm0_a3: string; };
  geometry: {
    type: string;
    coordinates: [number, number][];
  };
};

const Map = () => {
  const data: any = GeoJsonData;

  return (
    <>
      <Head>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css" integrity="sha256-kLaT2GOSpHechhsozzB+flnD+zUyjE2LlfWPgU04xyI=" crossOrigin="" />
      </Head>
      <Script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js" integrity="sha256-WBkoXOwTeyKclOHuWtc+i2uENFpDZ9YPdf5Hf+D7ewM=" crossOrigin=""></Script>
      <div style={{ aspectRatio: (1000 / 400).toString() }}>
        <MapContainer center={[51.505, -0.09]} zoom={3} minZoom={2} scrollWheelZoom={false} className="h-full w-full">
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          {/* <Marker position={[51.505, -0.09]}>
            <Popup>
              A pretty CSS3 popup. <br /> Easily customizable.
            </Popup>
          </Marker> */}
          {data.features
            .filter((geo: TGeo) => geo.properties.adm0_a3 === "GBR")
            .map((geo: TGeo) => {
              return <Polygon pathOptions={geoOptions} positions={geo.geometry.coordinates} key={geo.properties.adm0_a3} />;
            })}
        </MapContainer>
      </div>
    </>
  );
};

export default Map;
