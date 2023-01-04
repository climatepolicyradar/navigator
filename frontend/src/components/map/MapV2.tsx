import Script from "next/script";
import Head from "next/head";
import { MapContainer, Marker, Popup } from "react-leaflet";

// export const Map = () => {
//   return (
//     <>
//       <Head>
//         <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css" integrity="sha256-kLaT2GOSpHechhsozzB+flnD+zUyjE2LlfWPgU04xyI=" crossOrigin="" />
//       </Head>
//       <Script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js" integrity="sha256-WBkoXOwTeyKclOHuWtc+i2uENFpDZ9YPdf5Hf+D7ewM=" crossOrigin=""></Script>
//       <div id="map" className="h-[600px] w-full">
//         <MapContainer center={[51.505, -0.09]} zoom={13} scrollWheelZoom={false}>
//           {/* <Marker position={[51.505, -0.09]}>
//             <Popup>
//               A pretty CSS3 popup. <br /> Easily customizable.
//             </Popup>
//           </Marker> */}
//           {({ TileLayer, Marker, Popup }) => (
//             <>
//               <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors' />
//               <Marker position={DEFAULT_CENTER}>
//                 <Popup>
//                   A pretty CSS3 popup. <br /> Easily customizable.
//                 </Popup>
//               </Marker>
//             </>
//           )}
//         </MapContainer>
//       </div>
//     </>
//   );
// };

import dynamic from "next/dynamic";

const DynamicMap = dynamic(() => import("./DynamicMap"), {
  ssr: false,
});

const Map = (props) => {
  // const { width = DEFAULT_WIDTH, height = DEFAULT_HEIGHT } = props;
  return (
    <>
      <Head>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css" integrity="sha256-kLaT2GOSpHechhsozzB+flnD+zUyjE2LlfWPgU04xyI=" crossOrigin="" />
      </Head>
      <Script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js" integrity="sha256-WBkoXOwTeyKclOHuWtc+i2uENFpDZ9YPdf5Hf+D7ewM=" crossOrigin=""></Script>
      <div style={{ aspectRatio: (1000 / 400).toString() }}>
        <DynamicMap {...props} />
      </div>
    </>
  );
};

export default Map;
