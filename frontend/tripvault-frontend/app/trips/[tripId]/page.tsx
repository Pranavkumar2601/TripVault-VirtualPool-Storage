"use client";

import { useParams } from "next/navigation";
import InviteMember from "./invite";
import Files from "./files";
import Quota from "./quota";

export default function TripPage() {
  const params = useParams();
  const tripId = params.tripId as string;

  return (
    <div>
      <h2>Trip Workspace</h2>
      <p>Trip ID: {tripId}</p>

      <Quota tripId={tripId} />
      <InviteMember tripId={tripId} />
      <Files tripId={tripId} />
    </div>
  );
}
