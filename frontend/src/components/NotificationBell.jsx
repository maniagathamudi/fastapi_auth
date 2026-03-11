import { useEffect, useState } from "react"
import axios from "axios"
import "./notification.css"

const NotificationBell = () => {

    const [notifications,setNotifications] = useState([])
    const [unread,setUnread] = useState(0)
    const [open,setOpen] = useState(false)

    const token = localStorage.getItem("token")

    const fetchNotifications = async () => {
        try{
            const res = await axios.get(
                "http://127.0.0.1:8000/dashboard/notifications",
                {
                    headers:{
                        Authorization:`Bearer ${token}`
                    }
                }
            )
            setNotifications(res.data)
        }
        catch(err){
            console.log(err)
        }
    }

    const fetchUnread = async () => {
        try{
            const res = await axios.get(
                "http://127.0.0.1:8000/dashboard/notifications/unread-count",
                {
                    headers:{
                        Authorization:`Bearer ${token}`
                    }
                }
            )
            setUnread(res.data.unread_count)
        }
        catch(err){
            console.log(err)
        }
    }

    const markAllRead = async () => {

        await axios.put(
            "http://127.0.0.1:8000/dashboard/notifications/read-all",
            {},
            {
                headers:{
                    Authorization:`Bearer ${token}`
                }
            }
        )

        fetchNotifications()
        fetchUnread()
    }

    useEffect(()=>{
        fetchNotifications()
        fetchUnread()
    },[])

    return (

        <div className="notification-container">

            <div
                className="bell-icon"
                onClick={()=>setOpen(!open)}
            >
                🔔

                {unread > 0 && (
                    <span className="badge">{unread}</span>
                )}

            </div>

            {open && (

                <div className="notification-dropdown">

                    <div className="notification-header">

                        <h4>Notifications</h4>

                        <button onClick={markAllRead}>
                            Mark All Read
                        </button>

                    </div>

                    {notifications.length === 0 ? (

                        <p className="empty">
                            No notifications
                        </p>

                    ) : (

                        notifications.map((n,i)=>(
                            <div
                                key={i}
                                className={
                                    n.is_read
                                    ? "notification-item"
                                    : "notification-item unread"
                                }
                            >

                                <p>{n.message}</p>

                                <span>
                                    {new Date(n.created_at).toLocaleString()}
                                </span>

                            </div>
                        ))

                    )}

                </div>

            )}

        </div>

    )
}

export default NotificationBell