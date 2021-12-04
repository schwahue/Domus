import React from "react";
import AdminLayout from "../components/layouts/admin";
import TicketingTable from "../components/Admin-Dashboard/Ticketing/ticketing-table";

const TicketingApp = () => {
    return (
        <AdminLayout title="Ticketing">
            <TicketingTable />
        </AdminLayout>
    )
}

export default TicketingApp