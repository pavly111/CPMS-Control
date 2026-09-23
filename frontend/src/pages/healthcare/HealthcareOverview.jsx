import React, { useEffect, useState } from 'react';
import { Plus, Activity, HeartPulse } from 'lucide-react';
import { Link } from 'react-router-dom';
import styles from '../PrisonStyles.module.css';
import { hasRole } from '../../services/authentication';

export const HealthcareOverview = () => {
  const [prisonId, setPrisonId] = useState(undefined);
  const [data, setData] = useState({ doctors: [], visits: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const resolvePrison = async () => {
      try {
        let pid;
        if (hasRole('manager')) {
          const nationalId = localStorage.getItem('userNationalId') || '';
          const prisonRes = await fetch(`/api/prison/user/${nationalId}`);
          const prisonData = await prisonRes.json();
          pid = prisonData?.prison_id;
        } else {
          pid = localStorage.getItem('prison_id');
        }
        setPrisonId(pid ?? null);
      } catch {
        setPrisonId(null);
        setLoading(false);
      }
    };
    resolvePrison();
  }, []);

  useEffect(() => {
    if (prisonId === undefined) return;
    const doctorUrl = prisonId ? `/api/doctor/prison/${prisonId}` : '/api/doctor';
    const visitUrl = prisonId ? `/api/medical-visit/prison/${prisonId}` : '/api/medical-visit';
    Promise.all([
      fetch(doctorUrl).then(r => r.json()),
      fetch(visitUrl).then(r => r.json()),
    ]).then(([doctors, visits]) => {
      setData({ doctors, visits });
      setLoading(false);
    }).catch(() => setLoading(false));
  }, [prisonId]);

  if (loading) return <div className={styles.emptyState}>Loading Healthcare Records...</div>;

  return (
    <div className={styles.prisonContainer}>
      <div className={styles.wallBackground} aria-hidden="true">
        <div className={styles.wallGrain} />
        <div className={styles.blockLines} />
        <div className={styles.stainOne} />
        <div className={styles.stainTwo} />
        <div className={styles.lightTube} />
        <div className={styles.lightCone} />
      </div>
      <div className={styles.flickerLight} aria-hidden="true" />
      <div className={styles.barOverlay} aria-hidden="true">
        {[0, 1, 2].map((bar) => <div key={bar} className={styles.bar} />)}
      </div>

      <div className={styles.prisonContent}>
        <header className={styles.prisonHeader}>
          <h1 className={styles.prisonTitle}>Healthcare</h1>
        </header>

        <div className={styles.ledger}>
          <div className={styles.ledgerTitle}><HeartPulse size={16} style={{ marginRight: '6px' }} /> Doctors</div>
          <div className={styles.tableWrapper}>
            <table className={styles.table}>
              <thead><tr><th>National ID</th><th>Name</th><th>Address</th><th>Phone</th><th>Prison</th></tr></thead>
              <tbody>
                {data.doctors.length > 0 ? data.doctors.map((doc) => (
                  <tr key={doc.national_id}>
                    <td>{doc.national_id}</td>
                    <td>{doc.name}</td>
                    <td>{doc.address || '—'}</td>
                    <td>{doc.phone || '—'}</td>
                    <td>{doc.prison_name}</td>
                  </tr>
                )) : (
                  <tr><td colSpan="5" className={styles.emptyState}>No doctors registered.</td></tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        <div className={styles.detailPanel}>
          <h3><Activity size={16} style={{ marginRight: '6px' }} /> Medical Visit Records</h3>
          <div className={styles.tableWrapper}>
            <table className={styles.table}>
              <thead><tr><th>ID</th><th>Inmate</th><th>Doctor</th><th>Date/Time</th><th>Diagnosis</th><th>Notes</th></tr></thead>
              <tbody>
                {data.visits.length > 0 ? data.visits.map((v) => (
                  <tr key={v.visit_id}>
                    <td>{v.visit_id}</td>
                    <td>{v.inmate_name}</td>
                    <td>{v.doctor_name}</td>
<td>
                    {v.visit_datetime
                      ? new Date(v.visit_datetime).toLocaleString()
                      : '—'
                    }
                  </td>
                  <td>{v.diagnosis || '—'}</td>
                  <td style={{ fontSize: '0.8rem' }}>{v.description || '—'}</td>
                  </tr>
                )) : (
                  <tr><td colSpan="6" className={styles.emptyState}>No medical visits recorded.</td></tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {hasRole('admin') && (
          <div style={{ textAlign: 'center', marginTop: '20px' }}>
            <Link to="/healthcare/doctors/add" className={`${styles.btn} ${styles.btnPrimary}`}>
              <Plus size={16} /> Add Doctor
            </Link>
          </div>
        )}
        {hasRole('manager') && (
          <div style={{ textAlign: 'center', marginTop: '20px' }}>
            <Link to="/healthcare/visits/add" className={`${styles.btn} ${styles.badgeSuccess}`} style={{ textDecoration: 'none' }}>
              <Plus size={16} /> Record Medical Visit
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};